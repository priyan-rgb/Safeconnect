from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base

from app.models import user
from app.models import complaint
from app.models import emergency_contact
from app.models import notification
from app.models import emergency

from app.api.users import router as user_router
from app.api.complaints import router as complaint_router
from app.api.admin import router as admin_router
from app.api.legal import router as legal_router
from app.api.emergency import router as emergency_router
from app.api.emergency_contacts import router as emergency_contacts_router
from app.api.notifications import router as notifications_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SafeConnect API",
    description="AI-Powered Smart Safety, Legal Assistance & Grievance Resolution Platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(complaint_router)
app.include_router(admin_router)
app.include_router(legal_router)
app.include_router(emergency_router)
app.include_router(emergency_contacts_router)
app.include_router(notifications_router)


@app.get("/")
def home():
    return {
        "message": "SafeConnect Backend Running Successfully"
    }