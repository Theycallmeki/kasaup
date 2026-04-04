from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    receiver_id: int 


class Message(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    sender_name: str
    is_read: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationBase(BaseModel):
    user_id: int
    provider_id: int


class Conversation(ConversationBase):
    id: int
    last_message: Optional[str] = None
    updated_at: datetime
    provider_owner_id: int
    user_name: str
    shop_name: str
    provider_profile_image: Optional[str] = None
    user_profile_image: Optional[str] = None
    unread_count: int = 0
    

    model_config = ConfigDict(from_attributes=True)
