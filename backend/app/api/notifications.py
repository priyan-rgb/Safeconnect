from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.notification import Notification


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


class NotificationCreate(BaseModel):
    title: str
    message: str
    notification_type: str = "General"


@router.post("/")
def create_notification(
    data: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_notification = Notification(
        user_id=current_user.id,
        title=data.title,
        message=data.message,
        notification_type=data.notification_type,
        is_read="false"
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return {
        "message": "Notification created successfully",
        "notification_id": new_notification.id
    }


@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).all()

    return {
        "user_id": current_user.id,
        "notifications": [
            {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "is_read": notification.is_read
            }
            for notification in notifications
        ]
    }


@router.put("/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        return {
            "message": "Notification not found"
        }

    notification.is_read = "true"

    db.commit()

    return {
        "message": "Notification marked as read",
        "notification_id": notification.id
    }