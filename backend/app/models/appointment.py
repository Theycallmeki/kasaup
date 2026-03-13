from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)

    appointment_time = Column(DateTime)

    status = Column(String)

    user = relationship("User", back_populates="appointments")

    provider = relationship("Provider", back_populates="appointments")