from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, admin, public
from app.database import engine, Base
from app.models import *  # Импортируем все модели для создания таблиц

# Create tables
def init_db():
    """Инициализирует базу данных: создает все таблицы"""
    try:
        print("Создание таблиц в базе данных...")
        Base.metadata.create_all(bind=engine)
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

# Инициализируем БД при запуске
init_db()

app = FastAPI(
    title="Сириус API",
    description="API для корпоративного сайта Сириус",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3006",
        "https://itwin.kz",
        "http://itwin.kz",
        "https://www.itwin.kz",
        "http://www.itwin.kz"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(public.router, prefix="/api", tags=["public"])

# Import and include contact router
from app.api import contact
app.include_router(contact.router, prefix="/api", tags=["contact"])

@app.get("/")
async def root():
    return {"message": "Сириус API"}

@app.get("/health")
async def health():
    return {"status": "ok"}

