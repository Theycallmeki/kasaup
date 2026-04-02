from sqlalchemy import Column, Integer, String, DateTime
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

    created_at = Column(DateTime, default=get_ph_time)

    appointments = relationship("Appointment", back_populates="user")