"""
Скрипт для создания первого администратора
Использование: python scripts/create_admin.py
"""
import sys
import os

# Добавляем корневую директорию backend в путь
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(script_dir)
sys.path.insert(0, backend_dir)

# Устанавливаем рабочую директорию
os.chdir(backend_dir)

from app.database import SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash

def create_admin(email: str = None, password: str = None, full_name: str = None):
    """Создает администратора"""
    db = SessionLocal()
    
    try:
        # Запрашиваем данные, если не переданы
        if not email:
            email = input("Введите email администратора: ").strip()
        if not password:
            import getpass
            password = getpass.getpass("Введите пароль: ").strip()
            password_confirm = getpass.getpass("Подтвердите пароль: ").strip()
            if password != password_confirm:
                print("Пароли не совпадают!")
                return False
        if not full_name:
            full_name = input("Введите ФИО администратора: ").strip()
        
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"Пользователь с email {email} уже существует!")
            return False
        
        # Создаем администратора
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            is_superuser=True,
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"\n✓ Администратор успешно создан!")
        print(f"  Email: {admin.email}")
        print(f"  ФИО: {admin.full_name}")
        print(f"  ID: {admin.id}")
        
        return True
        
    except Exception as e:
        db.rollback()
        print(f"✗ Ошибка при создании администратора: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Создание администратора")
    print("=" * 50)
    
    # Можно передать параметры через аргументы командной строки
    if len(sys.argv) >= 4:
        email = sys.argv[1]
        password = sys.argv[2]
        full_name = sys.argv[3]
        create_admin(email, password, full_name)
    else:
        create_admin()
