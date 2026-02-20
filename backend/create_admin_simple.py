"""
Простой скрипт для создания администратора
Запуск: python create_admin_simple.py
"""
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, create_database_if_not_exists
from app.models.user import User
from app.services.auth import get_password_hash

def main():
    print("=" * 50)
    print("Создание администратора")
    print("=" * 50)
    
    # Убеждаемся, что БД существует
    create_database_if_not_exists()
    
    db = SessionLocal()
    
    try:
        # Запрашиваем данные
        email = input("\nВведите email администратора: ").strip()
        if not email:
            print("Email не может быть пустым!")
            return
        
        # Проверяем, существует ли пользователь
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"\n⚠ Пользователь с email {email} уже существует!")
            response = input("Хотите обновить пароль? (y/n): ").strip().lower()
            if response == 'y':
                import getpass
                password = getpass.getpass("Введите новый пароль: ").strip()
                password_confirm = getpass.getpass("Подтвердите пароль: ").strip()
                if password != password_confirm:
                    print("Пароли не совпадают!")
                    return
                existing_user.hashed_password = get_password_hash(password)
                existing_user.is_superuser = True
                existing_user.is_active = True
                db.commit()
                print(f"\n✓ Пароль администратора обновлен!")
                print(f"  Email: {existing_user.email}")
                return
            else:
                return
        
        import getpass
        password = getpass.getpass("Введите пароль: ").strip()
        password_confirm = getpass.getpass("Подтвердите пароль: ").strip()
        if password != password_confirm:
            print("Пароли не совпадают!")
            return
        
        # Проверка длины пароля (bcrypt ограничивает 72 байтами)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            print(f"\n⚠ Внимание: Пароль слишком длинный ({len(password_bytes)} байт).")
            print("Bcrypt ограничивает пароль 72 байтами. Пароль будет обрезан.")
            response = input("Продолжить? (y/n): ").strip().lower()
            if response != 'y':
                return
        
        full_name = input("Введите ФИО администратора: ").strip()
        if not full_name:
            full_name = "Администратор"
        
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
        print(f"  Суперпользователь: {admin.is_superuser}")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ Ошибка при создании администратора: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()

