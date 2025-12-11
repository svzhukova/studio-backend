from fastapi import APIRouter
from pydantic import BaseModel

# Роутер без собственного prefix — он будет задан в main.py
router = APIRouter(tags=["Users"])

# Модель пользователя для POST-запросов
class User(BaseModel):
    username: str
    email: str
    password: str

# GET /users/ — тестовый эндпоинт
@router.get("/")
def get_users():
    return {"users": ["Alice", "Bob"]}

# POST /users/register
@router.post("/register")
def register_user(user: User):
    return {"status": "ok", "user": user}

# POST /users/login
@router.post("/login")
def login(user: User):
    # В реальном проекте тут будет проверка пароля
    return {"status": "logged_in", "user": user.username}
