from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import List
from datetime import datetime

from database import get_db
from models.booking import Booking
from auth import SECRET_KEY, ALGORITHM

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

def get_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен"
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен"
        )

security = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    return get_user_id_from_token(credentials.credentials)

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_data: BookingCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

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
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):

    bookings = db.query(Booking).filter(
        Booking.user_id == user_id
    ).order_by(Booking.class_date, Booking.class_time).all()
    
    return bookings

@router.delete("/{booking_id}", status_code=status.HTTP_200_OK)
def cancel_booking(
    booking_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Отмена записи на занятие
    """
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()
    
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Запись не найдена"
        )
    
    db.delete(booking)
    db.commit()
    
    return {"message": "Запись успешно отменена"}