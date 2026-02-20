from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Danil228@localhost:5440/sirius_db"
)

# Извлекаем параметры подключения для создания БД
def parse_db_url(url: str):
    """Парсит DATABASE_URL и возвращает компоненты"""
    # Формат: postgresql://user:password@host:port/dbname
    url = url.replace("postgresql://", "")
    if "@" in url:
        auth, rest = url.split("@", 1)
        user, password = auth.split(":", 1)
    else:
        user, password = "postgres", ""
        rest = url
    
    if ":" in rest:
        host_port, dbname = rest.split("/", 1)
        if ":" in host_port:
            host, port = host_port.split(":", 1)
        else:
            host, port = host_port, "5432"
    else:
        host, port = rest.split("/", 1)[0], "5432"
        dbname = rest.split("/", 1)[1] if "/" in rest else "postgres"
    
    return {
        "user": user,
        "password": password,
        "host": host,
        "port": port,
        "dbname": dbname
    }

def create_database_if_not_exists():
    """Создает базу данных, если она не существует"""
    try:
        db_params = parse_db_url(DATABASE_URL)
        
        # Подключаемся к системной БД postgres для создания новой БД
        admin_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/postgres"
        
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
        
        with admin_engine.connect() as conn:
            # Проверяем, существует ли БД (используем параметризованный запрос для безопасности)
            result = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": db_params['dbname']}
            )
            exists = result.fetchone()
            
            if not exists:
                print(f"Создание базы данных {db_params['dbname']}...")
                try:
                    # Пробуем создать БД с template0 (всегда доступен)
                    dbname_quoted = db_params['dbname'].replace('"', '""')  # Экранируем кавычки
                    conn.execute(text(f'CREATE DATABASE "{dbname_quoted}" WITH TEMPLATE template0'))
                    print(f"✓ База данных {db_params['dbname']} успешно создана!")
                except Exception as create_error:
                    # Если не получилось с template0, пробуем без указания template
                    try:
                        conn.execute(text(f'CREATE DATABASE "{dbname_quoted}"'))
                        print(f"✓ База данных {db_params['dbname']} успешно создана!")
                    except Exception as create_error2:
                        print(f"⚠ Не удалось создать БД автоматически: {create_error2}")
                        print("Попробуйте создать БД вручную:")
                        print(f"  CREATE DATABASE {db_params['dbname']};")
                        print("Или закройте другие подключения к PostgreSQL и попробуйте снова.")
                        admin_engine.dispose()
                        return False
            else:
                print(f"✓ База данных {db_params['dbname']} уже существует.")
        
        admin_engine.dispose()
        return True
    except Exception as e:
        print(f"⚠ Ошибка при создании базы данных: {e}")
        print("Попробуйте создать БД вручную или проверьте права доступа.")
        db_params = parse_db_url(DATABASE_URL)
        print(f"Команда для ручного создания: CREATE DATABASE {db_params.get('dbname', 'sirius_db')};")
        # Не прерываем выполнение, возможно БД уже существует
        return False

# Создаем БД при импорте модуля (можно отключить, установив AUTO_CREATE_DB=false в .env)
# Это нужно для автоматического создания БД при первом запуске
if os.getenv("AUTO_CREATE_DB", "true").lower() == "true":
    try:
        create_database_if_not_exists()
    except Exception as e:
        # Не прерываем выполнение, если не удалось создать БД
        # Пользователь может создать её вручную
        pass

# Создаем engine для основной БД
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
