from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None
    appointment_id: Optional[int] = None


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    comment: Optional[str] = None


class Review(ReviewBase):
    id: int
    user_id: int
    provider_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
