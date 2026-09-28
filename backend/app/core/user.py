from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def test_users():
    return {
        "message": "User API working"
    }