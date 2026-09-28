from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.security import hash_password, verify_password
from app.utils.auth import create_access_token
from app.core.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users():
    return {
        "message": "Users API working"
    }


@router.post("/register", response_model=UserResponse)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        hashed_password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



@router.get("/profile", response_model=UserResponse)
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user