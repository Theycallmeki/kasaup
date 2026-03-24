from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class ServiceImage(Base):
    __tablename__ = "service_images"

    id = Column(Integer, primary_key=True, index=True)

    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))

    image_url = Column(String, nullable=False)

    service = relationship("Service", back_populates="images")