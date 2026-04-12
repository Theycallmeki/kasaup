import re
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

# PH mobile: +639XXXXXXXXX (10 digits after +63, starting with 9)
_PH_PHONE_RE = re.compile(r'^\+639\d{9}$')


def _normalize_phone(v: str | None) -> str | None:
    """Normalize phone to +63XXXXXXXXXX form, rejects non-PH numbers."""
    if v is None or v.strip() == '':
        return None
    stripped = re.sub(r'[\s\-()]', '', v.strip())
    if re.fullmatch(r'\+639\d{9}', stripped):
        return stripped
    if re.fullmatch(r'09\d{9}', stripped):
        return '+63' + stripped[1:]
    if re.fullmatch(r'639\d{9}', stripped):
        return '+' + stripped
    raise ValueError(
        'Phone must be a valid Philippine number (e.g. +63 912 345 6789 or 09123456789).'
    )


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    phone: str | None = None
    role: str | None = "customer"
    address: str | None = None

    @field_validator('password')
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters.')
        return v

    @field_validator('full_name')
    @classmethod
    def full_name_not_empty(cls, v: str | None) -> str | None:
        if v is not None and v.strip() == '':
            raise ValueError('Full name cannot be blank.')
        return v.strip() if v else v

    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        return _normalize_phone(v)


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    address: str | None = None

    @field_validator('password')
    @classmethod
    def password_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters.')
        return v

    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        return _normalize_phone(v)


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