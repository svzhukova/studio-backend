from fastapi import APIRouter

router = APIRouter(prefix="/abonements", tags=["Abonements"])

@router.get("/")
def get_abonements():
    return [
        {"id": 1, "title": "Разовое посещение", "price": 700},
        {"id": 2, "title": "Абонемент 8 занятий", "price": 4800},
        {"id": 3, "title": "Неограниченный месяц", "price": 5500},
    ]


