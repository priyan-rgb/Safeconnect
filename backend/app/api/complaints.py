from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.models.notification import Notification
from app.schemas.complaint import ComplaintCreate, ComplaintResponse
from app.core.security import get_current_user, get_current_admin
from app.services.ai_service import analyze_complaint


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"]
)


ALLOWED_STATUSES = {
    "Pending",
    "Under Review",
    "In Progress",
    "Resolved",
    "Escalated"
}


@router.post("/", response_model=ComplaintResponse)
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ai_result = analyze_complaint(complaint.description)

    new_complaint = Complaint(
        title=complaint.title,
        description=complaint.description,
        location=complaint.location,
        category=ai_result["category"],
        ai_category=ai_result["category"],
        priority=ai_result["priority"],
        authority=ai_result["authority"],
        status="Pending",
        user_id=current_user.id
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return new_complaint


@router.get("/", response_model=list[ComplaintResponse])
def get_my_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    complaints = db.query(Complaint).filter(
        Complaint.user_id == current_user.id
    ).all()

    return complaints


@router.get("/all", response_model=list[ComplaintResponse])
def get_all_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    complaints = db.query(Complaint).all()

    return complaints


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint_by_id(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    if (
        complaint.user_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view this complaint"
        )

    return complaint


@router.put("/{complaint_id}/status")
def update_complaint_status(
    complaint_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Invalid complaint status",
                "allowed_statuses": list(ALLOWED_STATUSES)
            }
        )

    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found"
        )

    complaint.status = status

    new_notification = Notification(
        user_id=complaint.user_id,
        title="Complaint Status Updated",
        message=f"Your complaint '{complaint.title}' is now '{status}'.",
        notification_type="Complaint",
        is_read="false"
    )

    db.add(new_notification)

    db.commit()
    db.refresh(complaint)

    return {
        "message": "Complaint status updated successfully",
        "complaint_id": complaint.id,
        "new_status": complaint.status,
        "notification_created": True
    }