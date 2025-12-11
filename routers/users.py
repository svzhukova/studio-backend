from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register():
    return {"message": "User registered"}

@router.post("/register")
def register_user(user: dict):
    return {"status": "ok", "user": user}