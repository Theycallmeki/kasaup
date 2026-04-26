import re
from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime


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


class ProviderCreate(BaseModel):
    shop_name: str
    description: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    latitude: float
    longitude: float
    offers_home_service: bool

    @field_validator('shop_name')
    @classmethod
    def shop_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Shop name is required.')
        return v.strip()

    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        return _normalize_phone(v)


class ProviderUpdate(BaseModel):
    shop_name: str | None = None
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    offers_home_service: bool | None = None

    @field_validator('shop_name')
    @classmethod
    def shop_name_not_empty(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError('Shop name cannot be blank.')
        return v.strip() if v else v

    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        return _normalize_phone(v)

    class Config:
        from_attributes = True


class ProviderResponse(BaseModel):
    id: int
    owner_id: int | None = None
    shop_name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    latitude: float
    longitude: float
    offers_home_service: bool
    profile_image: str | None = None
    rating: float | None = None
    total_reviews: int | None = None
    is_verified: bool | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class ProviderListItem(ProviderResponse):
    service_names: list[str] = []
    category_names: list[str] = []