from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):
    provider_id: int
    service_id: int
    appointment_time: datetime
    customer_latitude: float | None = None
    customer_longitude: float | None = None


class AppointmentUpdate(BaseModel):
    appointment_time: datetime | None = None


class AppointmentResponse(BaseModel):
    id: int
    user_id: int
    provider_id: int
    service_id: int
    appointment_time: datetime
    status: str
    customer_latitude: float | None = None
    customer_longitude: float | None = None

    class Config:
        from_attributes = True