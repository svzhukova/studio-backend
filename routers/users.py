from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class User(BaseModel):
    username: str
    email: str

# Первый роут
@router.post("/register")
def register_user(user: User):
    return {"status": "ok", "user": user}

# Второй роут с другим путём
@router.post("/login")
def login(user: User):
    return {"status": "logged_in", "user": user.username}
