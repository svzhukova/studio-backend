from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os  
from fastapi.staticfiles import StaticFiles
from routers.bookings import router as bookings_router
from jose import jwt
from datetime import timedelta

SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI(title="Yoga Studio API", version="1.0")
app.include_router(bookings_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://127.0.0.1:5173",  
        "https://studio-backend-8rnj.onrender.com",  
        "*" 
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    """Получаем токен из заголовка Authorization"""
    if not token:
        return None
    return {
        "id": 1,
        "email": "test@example.com",
        "first_name": "Иван",
        "last_name": "Иванов",
        "phone": "+7 999 123-45-67",
        "created_at": datetime.now().isoformat()
    }


@app.get("/")
def root():
    return {"message": "API работает!", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/auth/login")
def login(user: UserLogin):
    user_data = {
        "sub": "1",  # user.id
        "email": user.email
    }
    access_token = create_access_token(user_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": 1,
            "email": user.email,
            "first_name": "Иван",
            "last_name": "Иванов",
            "phone": "+7 999 123-45-67",
            "created_at": datetime.now().isoformat()
        }
    }

@app.post("/auth/register")
def register(user: UserRegister):
    print(f"👤 Регистрация: {user.first_name} {user.last_name} ({user.email})")
    return {
        "success": True,
        "message": "Регистрация успешна!",
        "user": {
            "id": 2,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
            "created_at": datetime.now().isoformat()
        },
        "access_token": f"reg-token-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "token_type": "bearer"
    }

@app.get("/auth/me")
def get_profile(current_user: Optional[dict] = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Требуется авторизация")
    return current_user



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")


app.include_router(bookings_router)


if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="static")