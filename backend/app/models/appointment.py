from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)

    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    appointment_time = Column(DateTime, nullable=False)

    status = Column(String, default="pending", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="appointments")

    provider = relationship("Provider", back_populates="appointments")

    service = relationship("Service")
