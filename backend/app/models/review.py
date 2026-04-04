from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.core.timezone import get_ph_time


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"), unique=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    
    rating = Column(Float, nullable=False) # 1.0 to 5.0
    comment = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=get_ph_time)

   
    user = relationship("User", back_populates="reviews")
    provider = relationship("Provider", back_populates="reviews")
    appointment = relationship("Appointment", back_populates="review")
