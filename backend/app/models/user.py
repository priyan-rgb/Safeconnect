from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    phone = Column(String, unique=True, nullable=True)

    hashed_password = Column(String, nullable=False)

    role = Column(String, default="citizen")

    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship(
        "Complaint",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    emergency_contacts = relationship(
        "EmergencyContact",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )