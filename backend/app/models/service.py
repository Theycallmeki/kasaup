from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float)
    duration_minutes = Column(Integer)

    provider = relationship("Provider", back_populates="services")
    category = relationship("Category", back_populates="services")
    images = relationship("ServiceImage", back_populates="service", cascade="all, delete-orphan")

    # If service is deleted, its appointments should also be removed.
    appointments = relationship("Appointment", back_populates="service", cascade="all, delete-orphan")