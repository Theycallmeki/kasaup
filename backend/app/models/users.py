from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base
from app.core.timezone import get_ph_time


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)

    full_name = Column(String)

    phone = Column(String)

    role = Column(String, nullable=False, default="customer")
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=get_ph_time)

    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")
    
    
    provided_shop = relationship("Provider", back_populates="owner", cascade="all, delete-orphan", uselist=False)
    
    
    sent_messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    
    conversations = relationship("Conversation", foreign_keys="Conversation.user_id", back_populates="user", cascade="all, delete-orphan")

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")