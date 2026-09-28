from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.emergency_contact import EmergencyContact


router = APIRouter(
    prefix="/emergency-contacts",
    tags=["Emergency Contacts"]
)


class EmergencyContactCreate(BaseModel):
    name: str
    phone: str
    relationship: str


@router.post("/")
def add_emergency_contact(
    data: EmergencyContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_contact = EmergencyContact(
        name=data.name,
        phone=data.phone,
        relationship=data.relationship,
        user_id=current_user.id
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": "Emergency contact added successfully",
        "contact_id": new_contact.id,
        "user_id": current_user.id,
        "contact": {
            "name": new_contact.name,
            "phone": new_contact.phone,
            "relationship": new_contact.relationship
        }
    }


@router.get("/")
def get_emergency_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    contacts = db.query(EmergencyContact).filter(
        EmergencyContact.user_id == current_user.id
    ).all()

    return {
        "user_id": current_user.id,
        "contacts": [
            {
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone,
                "relationship": contact.relationship
            }
            for contact in contacts
        ]
    }