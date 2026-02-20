# Инструкция по настройке проекта

## Предварительные требования

- Node.js 18+ и npm
- Python 3.10+
- PostgreSQL 12+
- Git

## Быстрый старт

### 1. Клонирование и подготовка

```bash
# Клонируйте репозиторий (если есть)
git clone <repository-url>
cd sirius-web-lp-cursor
```

### 2. Настройка базы данных

1. Убедитесь, что PostgreSQL запущен
2. Создайте базу данных:
```sql
CREATE DATABASE sirius_db;
```

3. Проверьте подключение:
- Host: localhost
- Port: 5440
- User: postgres
- Password: Danil228
- Database: sirius_db

### 3. Настройка Backend

```bash
cd backend

# Создайте виртуальное окружение
python -m venv venv

# Активируйте виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Создайте файл .env
copy .env.example .env
# Или вручную создайте .env с содержимым:
# DATABASE_URL=postgresql://postgres:Danil228@localhost:5440/sirius_db
# SECRET_KEY=your-secret-key-change-in-production
# API_BASE_URL=http://localhost:8009

# База данных создастся автоматически при первом запуске
# Но можно создать вручную через скрипт:
python -m app.init_db
# или из корня backend:
cd backend
python -m app.init_db

# Выполните миграции (опционально, если используете Alembic)
# alembic upgrade head

# Создайте первого администратора
python scripts/create_admin.py

# Запустите сервер
python run.py
# или
uvicorn app.main:app --reload --port 8009
```

### 4. Настройка Frontend

```bash
cd frontend

# Скопируйте изображения
copy ..\logo.png public\
copy ..\main-func.png public\

# Установите зависимости
npm install

# Создайте файл .env
echo API_BASE_URL=http://localhost:8009 > .env

# Запустите dev сервер
npm run dev
```

### 5. Создание первого администратора

После запуска backend, создайте первого пользователя через API:

```bash
curl -X POST "http://localhost:8009/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@itwin.kz",
    "password": "your-secure-password",
    "full_name": "Администратор"
  }'
```

Или используйте Python:

```python
from app.database import SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash

db = SessionLocal()
admin = User(
    email="admin@itwin.kz",
    hashed_password=get_password_hash("your-secure-password"),
    full_name="Администратор",
    is_superuser=True
)
db.add(admin)
db.commit()
```

## Проверка работы

1. Frontend должен быть доступен на http://localhost:3006
2. Backend API должен быть доступен на http://localhost:8009
3. API документация (Swagger): http://localhost:8009/docs
4. Production сайт: https://itwin.kz (после настройки nginx)

## Структура базы данных

После выполнения миграций будут созданы следующие таблицы:
- `users` - пользователи системы
- `content_items` - элементы контента
- `media_files` - медиа файлы
- `demo_requests` - заявки на демо
- `seo_metadata` - SEO метатеги
- `pages` - страницы сайта
- `sections` - секции страниц

## Troubleshooting

### Ошибка подключения к БД
- Проверьте, что PostgreSQL запущен
- Убедитесь, что порт 5440 доступен
- Проверьте учетные данные в .env

### Ошибки при установке зависимостей
- Убедитесь, что используете правильную версию Python (3.10+)
- Для frontend: используйте Node.js 18+

### Проблемы с Vuetify
- Убедитесь, что все компоненты правильно импортированы в `plugins/vuetify.ts`
- Проверьте, что tree-shaking настроен корректно

## Production деплой

### Backend
1. Установите зависимости в production окружении
2. Настройте переменные окружения
3. Используйте production WSGI сервер (например, Gunicorn)
4. Настройте reverse proxy (Nginx)

### Frontend
1. Выполните `npm run build`
2. Используйте `npm run preview` для проверки
3. Деплойте `.output/public` на статический хостинг
4. Или используйте SSR с Node.js сервером

## Домен

После деплоя настройте домен **itwin.kz** на ваш сервер.

