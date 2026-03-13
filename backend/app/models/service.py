from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    provider_id = Column(Integer, ForeignKey("providers.id"))

    category_id = Column(Integer, ForeignKey("categories.id"))

    name = Column(String, nullable=False)

    description = Column(String)

    price = Column(Float)

    duration_minutes = Column(Integer)

    provider = relationship("Provider", back_populates="services")

    category = relationship("Category", back_populates="services")