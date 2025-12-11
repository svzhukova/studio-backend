from fastapi import APIRouter

from models import schedule

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/")
def get_schedule():
    return [
        {"id": 1, "title": "Хатха-йога", "instructor": "Мария", "time": "10:00"},
        {"id": 2, "title": "Растяжка", "instructor": "Анна", "time": "12:00"},
    ]
@router.get("/")
def get_schedule():
    return schedule