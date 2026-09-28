from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database.database import Base


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    message = Column(Text, nullable=False)

    status = Column(String(50), default="ACTIVE")

    created_at = Column(DateTime(timezone=True), server_default=func.now())