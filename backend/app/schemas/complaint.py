from pydantic import BaseModel
from typing import Optional


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    priority: Optional[str] = None
    location: Optional[str] = None


class ComplaintResponse(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str] = None
    priority: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    user_id: int

    # AI Generated Fields
    ai_category: Optional[str] = None
    authority: Optional[str] = None

    class Config:
        from_attributes = True