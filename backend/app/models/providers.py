from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.core.timezone import get_ph_time


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    shop_name = Column(String, nullable=False)

    description = Column(String)

    phone = Column(String)

    email = Column(String)

    address = Column(String)

    latitude = Column(Float)

    longitude = Column(Float)

    offers_home_service = Column(Boolean, default=False)

    rating = Column(Float, default=0)

    total_reviews = Column(Integer, default=0)

    is_verified = Column(Boolean, default=False)

    profile_image = Column(String)  

    created_at = Column(DateTime, default=get_ph_time)

    owner = relationship("User")

    services = relationship("Service", back_populates="provider")

    appointments = relationship("Appointment", back_populates="provider")