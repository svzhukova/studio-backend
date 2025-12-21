from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./fitness_club.db"
    print("⚠️ DATABASE_URL не найден, использую SQLite")

# ← ДОБАВЬ ЭТУ СТРОКУ (алиас для Alembic)
SQLALCHEMY_DATABASE_URL = DATABASE_URL

if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
SQLALCHEMY_DATABASE_URL = DATABASE_URL
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()