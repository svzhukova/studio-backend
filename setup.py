import sys
import os

print("=" * 60)
print("НАСТРОЙКА БАЗЫ ДАННЫХ")
print("=" * 60)

# Добавляем путь
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
print(f"Добавлен путь: {current_dir}")

try:
    # Импортируем
    from database import engine, Base
    print("✅ Импортирован Base из database")
    
    # Импортируем модели
    try:
        from models import User, Booking
        print("✅ Импортированы модели")
    except ImportError:
        print("⚠️  Модели не найдены, создаем...")
        # Создаем models.py
        models_code = '''from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password_hash = Column(String)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer)
    class_name = Column(String)
    class_time = Column(String)
    class_date = Column(String)
    trainer_name = Column(String)
    hall_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())'''
        
        with open("models.py", "w") as f:
            f.write(models_code)
        
        from models import User, Booking
    
    # Создаем таблицы
    print("🔄 Создаем таблицы...")
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы созданы!")
    
    # Проверяем
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"📊 Таблицы в БД: {tables}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 60)
print("✅ НАСТРОЙКА ЗАВЕРШЕНА")
print("=" * 60)
