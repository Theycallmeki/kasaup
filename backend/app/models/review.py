from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.core.timezone import get_ph_time


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    appointment_id = Column(Integer, ForeignKey("appointments.id"), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    
    rating = Column(Float, nullable=False) # 1.0 to 5.0
    comment = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=get_ph_time)

   
    user = relationship("User")
    provider = relationship("Provider")
    appointment = relationship("Appointment")
