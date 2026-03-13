from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    provider_id: int
    appointment_time: datetime
    status: str = "pending"


class AppointmentUpdate(BaseModel):
    appointment_time: datetime | None = None
    status: str | None = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    provider_id: int
    appointment_time: datetime
    status: str

    class Config:
        from_attributes = True