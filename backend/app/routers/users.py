from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate, UserResponse, UserOut
from app.core.security import hash_password
from app.core.dependencies import require_admin, get_current_user
from app.services.upload_service import save_image
from app.services.email_service import send_approval_email, send_rejection_email

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = user.dict()
    user_data["password"] = hash_password(user.password)

    # New providers require admin approval
    if user_data.get("role") == "provider":
        user_data["is_approved"] = False

    new_user = User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.put("/me", response_model=UserOut)
def update_profile(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    if "email" in update_data and update_data["email"] != current_user.email:
        existing = db.query(User).filter(User.email == update_data["email"]).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already taken")

    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/profile-image/")
def upload_user_profile_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    path = save_image(file)
    current_user.profile_image = path
    db.commit()
    db.refresh(current_user)
    return {"url": path}


@router.get("/", response_model=list[UserResponse], dependencies=[Depends(require_admin)])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}/", response_model=UserResponse, dependencies=[Depends(require_admin)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/{user_id}/", response_model=UserResponse, dependencies=[Depends(require_admin)])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


@router.delete("/{user_id}/", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}


@router.put("/{user_id}/approve/", response_model=UserResponse, dependencies=[Depends(require_admin)])
def approve_user(user_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_approved = True
    db.commit()
    db.refresh(user)

    # Send approval email in background
    background_tasks.add_task(send_approval_email, user.email, user.full_name)

    return user


@router.put("/{user_id}/reject/", dependencies=[Depends(require_admin)])
def reject_user(user_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = user.email
    name = user.full_name

    # Delete the user
    db.delete(user)
    db.commit()

    # Send rejection email in background
    background_tasks.add_task(send_rejection_email, email, name)

    return {"message": "User rejected and deleted"}