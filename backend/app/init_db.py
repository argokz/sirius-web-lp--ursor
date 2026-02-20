"""
Скрипт для инициализации базы данных
Создает БД и все необходимые таблицы
"""
from app.database import create_database_if_not_exists, engine, Base
from app.models import *  # Импортируем все модели
import sys

def init_database():
    """Инициализирует базу данных"""
    print("=" * 50)
    print("Инициализация базы данных Сириус")
    print("=" * 50)
    
    # Создаем БД, если её нет
    if not create_database_if_not_exists():
        print("Не удалось создать базу данных. Проверьте настройки подключения.")
        sys.exit(1)
    
    # Создаем таблицы
    try:
        print("\nСоздание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("✓ Таблицы успешно созданы!")
        print("\nСписок созданных таблиц:")
        for table in Base.metadata.tables.keys():
            print(f"  - {table}")
    except Exception as e:
        print(f"\n✗ Ошибка при создании таблиц: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Инициализация завершена успешно!")
    print("=" * 50)

if __name__ == "__main__":
    init_database()

