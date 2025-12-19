from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/profile")
def get_profile(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получить профиль текущего пользователя"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """Получить пользователя по ID (для админа)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user