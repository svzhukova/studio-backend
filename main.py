from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os  
from database import engine
from models.user import Base
from fastapi.staticfiles import StaticFiles
from routers.bookings import router as bookings_router
from datetime import timedelta
from auth import router as auth_router

SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI(title="Yoga Studio API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://127.0.0.1:5173",  
        "https://studio-backend-8rnj.onrender.com",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
async def options_handler(path: str):
    return {}
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str

class BookingCreate(BaseModel):
    class_id: int
    class_name: str
    class_date: str
    class_time: str
    trainer_name: str

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "API работает!", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}





if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


app.include_router(bookings_router)


if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")
    


if __name__ == "__main__":
    import uvicorn
    from alembic import command
    from alembic.config import Config

    # Применяем миграции при запуске на Render
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))