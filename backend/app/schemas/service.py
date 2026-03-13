from pydantic import BaseModel


class ServiceCreate(BaseModel):
    provider_id: int
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int


class ServiceUpdate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: float
    duration_minutes: int


class ServiceResponse(BaseModel):
    id: int
    provider_id: int
    category_id: int
    name: str
    description: str | None
    price: float
    duration_minutes: int

    class Config:
        from_attributes = True