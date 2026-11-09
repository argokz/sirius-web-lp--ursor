import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import admin, auth, public
from app.database import Base, SessionLocal, engine
from app.models import *  # noqa: F401,F403 - импорт моделей нужен для create_all
from app.services.cms_seed import seed_cms_defaults


def init_db():
    """Создает таблицы и наполняет CMS стартовыми страницами."""
    try:
        print("Создание таблиц в базе данных...")
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        try:
            seed_cms_defaults(db)
        finally:
            db.close()

        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")


init_db()

# Описание API (Swagger/ReDoc) на проде закрыто: оно раскрывает все адреса админки.
api_docs_enabled = os.getenv("ENABLE_API_DOCS", "false").lower() == "true"

app = FastAPI(
    title="Сириус API",
    description="API для корпоративного сайта Сириус",
    version="1.0.0",
    docs_url="/docs" if api_docs_enabled else None,
    redoc_url="/redoc" if api_docs_enabled else None,
    openapi_url="/openapi.json" if api_docs_enabled else None,
)

# Создаем папку uploads, если её нет, и монтируем её для раздачи статики
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3006",
        "https://itwin.kz",
        "http://itwin.kz",
        "https://www.itwin.kz",
        "http://www.itwin.kz",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(public.router, prefix="/api", tags=["public"])

from app.api import contact

app.include_router(contact.router, prefix="/api", tags=["contact"])


@app.get("/")
async def root():
    return {"message": "Сириус API"}


@app.get("/health")
async def health():
    return {"status": "ok"}
