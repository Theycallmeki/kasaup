from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from datetime import datetime
import json
from app.core.timezone import get_ph_time

from app.db import get_db
from app.models.message import Conversation, Message
from app.models.users import User
from app.models.providers import Provider
from app.schemas.message import MessageCreate, Message as MessageSchema, Conversation as ConversationSchema
from app.core.dependencies import get_current_user
from app.services.websocket_manager import manager
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter()


@router.get("/test-cors")
def test_cors():
    return {"status": "CORS works for messages router"}


async def get_ws_user(websocket: WebSocket, db: Session):
    token = websocket.cookies.get("access_token")
    if not token:
        token = websocket.query_params.get("token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        return None


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    user = await get_ws_user(websocket, db)
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user.id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user.id)


@router.get("/conversations", response_model=List[ConversationSchema])
def get_conversations(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    my_providers = db.query(Provider).filter(Provider.owner_id == current_user.id).all()
    provider_ids = [p.id for p in my_providers]
    
    conversations = db.query(Conversation).filter(
        or_(
            Conversation.user_id == current_user.id,
            Conversation.provider_id.in_(provider_ids)
        )
    ).order_by(Conversation.updated_at.desc()).all()

    for convo in conversations:
        if convo.updated_at is None:
            convo.updated_at = get_ph_time()
        # Add provider_owner_id and names for schema fulfillment
        convo.provider_owner_id = convo.provider.owner_id
        convo.user_name = convo.user.full_name
        convo.shop_name = convo.provider.shop_name
        convo.provider_profile_image = convo.provider.profile_image

    return conversations


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageSchema])
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    provider = db.query(Provider).filter(Provider.id == conversation.provider_id).first()
    if conversation.user_id != current_user.id and (not provider or provider.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
    for msg in messages:
        msg.sender_name = msg.sender.full_name
    return messages


@router.post("/send", response_model=MessageSchema)
async def send_message(
    msg_in: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recipient = db.query(User).filter(User.id == msg_in.receiver_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # 1. Determine who is the customer and which provider is involved
    # Check if current_user is the provider
    current_provider = db.query(Provider).filter(Provider.owner_id == current_user.id).first()
    # Check if recipient is the provider
    recipient_provider = db.query(Provider).filter(Provider.owner_id == recipient.id).first()

    customer_id = None
    provider_id = None

    if current_provider and not recipient_provider:
        # Current user is provider, recipient is customer
        customer_id = recipient.id
        provider_id = current_provider.id
    elif not current_provider and recipient_provider:
        # Current user is customer, recipient is provider
        customer_id = current_user.id
        provider_id = recipient_provider.id
    else:
        # Both or neither are providers - might be a chat between two users who are both providers
        # but in this context, we need to know which provider profile we are chatting with.
        # If recipient is a provider, prioritize that.
        if recipient_provider:
            customer_id = current_user.id
            provider_id = recipient_provider.id
        else:
             raise HTTPException(status_code=400, detail="Cannot determine conversation parties. One must be a provider.")

    conversation = db.query(Conversation).filter(
        Conversation.user_id == customer_id,
        Conversation.provider_id == provider_id
    ).first()
    
    if not conversation:
        conversation = Conversation(user_id=customer_id, provider_id=provider_id)
        db.add(conversation)
        db.flush()

    db_msg = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        content=msg_in.content
    )
    db.add(db_msg)

    conversation.last_message = msg_in.content
    conversation.updated_at = db_msg.created_at

    db.commit()
    db.refresh(db_msg)

    # Populate sender_name for the return and websocket
    db_msg.sender_name = current_user.full_name

    msg_data = {
        "type": "new_message",
        "data": {
            "id": db_msg.id,
            "conversation_id": db_msg.conversation_id,
            "sender_id": db_msg.sender_id,
            "sender_name": db_msg.sender_name,
            "content": db_msg.content,
            "created_at": db_msg.created_at.isoformat()
        }
    }
    await manager.send_personal_message(msg_data, recipient.id)
    
    return db_msg


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    is_customer = conversation.user_id == current_user.id
    is_provider_owner = conversation.provider.owner_id == current_user.id
    
    if not is_customer and not is_provider_owner:
        raise HTTPException(status_code=403, detail="Not authorized to delete this conversation")
    
    db.delete(conversation)
    db.commit()
    return {"message": "Conversation deleted"}