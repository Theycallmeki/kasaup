from sqlalchemy import Column, Integer, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.db import Base


class ProviderAvailability(Base):
    __tablename__ = "provider_availability"

    id = Column(Integer, primary_key=True, index=True)

    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)

    day_of_week = Column(Integer, nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    provider = relationship("Provider")