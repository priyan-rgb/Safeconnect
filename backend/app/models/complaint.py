from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    category = Column(String, nullable=True)

    priority = Column(String, nullable=True)

    location = Column(String, nullable=True)

    status = Column(String, default="Pending")

    # AI Generated Fields
    ai_category = Column(String, nullable=True)

    authority = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="complaints")