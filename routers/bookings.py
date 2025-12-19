# routers/bookings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.booking import Booking
from pydantic import BaseModel
from typing import List
from datetime import datetime

# Импортируем зависимость из main.py
from main import get_current_user  # ← важно!

router = APIRouter(prefix="/bookings", tags=["Bookings"])

# Pydantic модели (без изменений)
class BookingCreate(BaseModel):
    class_id: int
    class_name: str
    class_time: str
    class_date: str
    trainer_name: str
    hall_name: str

class BookingResponse(BaseModel):
    id: int
    class_id: int
    class_name: str
    class_time: str
    class_date: str
    trainer_name: str
    hall_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Вспомогательная функция: получаем user_id из токена
def get_user_id_from_request(current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    return current_user["id"]  # ← у тебя в заглушке user["id"] = 1

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking_data: BookingCreate,
    user_id: int = Depends(get_user_id_from_request),  # ✅
    db: Session = Depends(get_db)
):
    # Проверка дубликата
    existing_booking = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.class_id == booking_data.class_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=400,
            detail="Вы уже записаны на это занятие"
        )
    
    # Создаём запись
    new_booking = Booking(
        user_id=user_id,
        class_id=booking_data.class_id,
        class_name=booking_data.class_name,
        class_time=booking_data.class_time,
        class_date=booking_data.class_date,
        trainer_name=booking_data.trainer_name,
        hall_name=booking_data.hall_name
    )
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/my", response_model=List[BookingResponse])
def get_my_bookings(
    user_id: int = Depends(get_user_id_from_request),  # ← из заголовка
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).order_by(Booking.class_date, Booking.class_time).all()
    return bookings

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    user_id: int = Depends(get_user_id_from_request),  # ← из заголовка
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    
    db.delete(booking)
    db.commit()
    return {"message": "Запись отменена"}