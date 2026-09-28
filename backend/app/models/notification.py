from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship as orm_relationship

from app.database.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    notification_type = Column(
        String,
        default="General"
    )

    is_read = Column(
        String,
        default="false"
    )

    user = orm_relationship(
        "User",
        back_populates="notifications"
    )