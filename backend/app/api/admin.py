from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.models.emergency import EmergencyAlert
from app.core.security import get_current_admin


router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)


@router.get("/dashboard")
def get_admin_dashboard(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    total_complaints = db.query(Complaint).count()

    pending_complaints = db.query(Complaint).filter(
        Complaint.status == "Pending"
    ).count()

    under_review_complaints = db.query(Complaint).filter(
        Complaint.status == "Under Review"
    ).count()

    in_progress_complaints = db.query(Complaint).filter(
        Complaint.status == "In Progress"
    ).count()

    resolved_complaints = db.query(Complaint).filter(
        Complaint.status == "Resolved"
    ).count()

    escalated_complaints = db.query(Complaint).filter(
        Complaint.status == "Escalated"
    ).count()

    high_priority_complaints = db.query(Complaint).filter(
        Complaint.priority == "High"
    ).count()

    category_results = db.query(
        Complaint.ai_category
    ).filter(
        Complaint.ai_category.isnot(None)
    ).all()

    category_statistics = {}

    for row in category_results:
        category = row[0]

        if category not in category_statistics:
            category_statistics[category] = 0

        category_statistics[category] += 1

    return {
        "total_complaints": total_complaints,
        "pending_complaints": pending_complaints,
        "under_review_complaints": under_review_complaints,
        "in_progress_complaints": in_progress_complaints,
        "resolved_complaints": resolved_complaints,
        "escalated_complaints": escalated_complaints,
        "high_priority_complaints": high_priority_complaints,
        "category_statistics": category_statistics
    }


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    users = db.query(User).order_by(User.id.desc()).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.get("/emergency-alerts")
def get_emergency_alerts(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    alerts = db.query(EmergencyAlert).order_by(
        EmergencyAlert.id.desc()
    ).all()

    return [
        {
            "id": alert.id,
            "user_id": alert.user_id,
            "latitude": alert.latitude,
            "longitude": alert.longitude,
            "message": alert.message,
            "status": alert.status,
            "created_at": alert.created_at
        }
        for alert in alerts
    ]