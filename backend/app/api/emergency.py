from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.security import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.models.emergency import EmergencyAlert


router = APIRouter(
    prefix="/emergency",
    tags=["Emergency Safety"]
)


class EmergencyRequest(BaseModel):
    latitude: float
    longitude: float
    message: str = "Emergency assistance required"


@router.post("/sos")
def send_sos(
    data: EmergencyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    emergency_alert = EmergencyAlert(
        user_id=current_user.id,
        latitude=data.latitude,
        longitude=data.longitude,
        message=data.message,
        status="ACTIVE"
    )

    db.add(emergency_alert)
    db.commit()
    db.refresh(emergency_alert)

    return {
        "message": "SOS alert activated successfully",
        "alert_id": emergency_alert.id,
        "user_id": current_user.id,
        "user_name": current_user.full_name,
        "latitude": data.latitude,
        "longitude": data.longitude,
        "emergency_message": data.message,
        "status": emergency_alert.status,
        "next_action": "Emergency contacts and nearby authorities should be notified."
    }