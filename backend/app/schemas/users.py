from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    phone: str | None = None
    role: str | None = "customer"


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone: str | None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone: str | None
    role: str
    created_at: datetime

    class Config:
        from_attributes = True