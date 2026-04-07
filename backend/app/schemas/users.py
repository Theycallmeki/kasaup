from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str | None = None
    phone: str | None = None
    role: str | None = "customer"
    address: str | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: str | None = None
    password: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone: str | None
    role: str
    latitude: float | None
    longitude: float | None
    address: str | None = None
    profile_image: str | None = None
    is_approved: bool = True
    has_profile: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone: str | None
    role: str
    latitude: float | None
    longitude: float | None
    address: str | None = None
    profile_image: str | None = None
    is_approved: bool = True
    has_profile: bool = False
    created_at: datetime

    class Config:
        from_attributes = True