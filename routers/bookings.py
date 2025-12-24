from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
from database import get_db
from models.booking import Booking
from models.user import User
from auth import get_current_user


router = APIRouter(prefix="/bookings", tags=["Bookings"])

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


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),  
    db: Session = Depends(get_db)
):
    user_id = current_user.id  

    existing_booking = db.query(Booking).filter(
        Booking.user_id == user_id,
        Booking.class_id == booking_data.class_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже записаны на это занятие"
        )
    
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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.class_date, Booking.class_time).all()
    
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == current_user.id  # ← безопасная проверка
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена или не принадлежит вам"
        )
    
    db.delete(booking)
    db.commit()
    
    return {"message": "Запись успешно отменена"}