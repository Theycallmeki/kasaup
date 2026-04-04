from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)

    appointment_time = Column(DateTime, nullable=False, index=True)

    duration_minutes = Column(Integer, nullable=False)

    status = Column(String, default="pending", nullable=False)

    customer_latitude = Column(Float, nullable=True)
    customer_longitude = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="appointments")
    provider = relationship("Provider", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    review = relationship("Review", back_populates="appointment", uselist=False)