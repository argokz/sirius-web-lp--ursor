# Сириус - Корпоративный сайт ТГИД-07

Многостраничный корпоративный сайт для компании Сириус с системой управления контентом (CRM).

## Технологический стек

### Frontend
- **Nuxt 4** - Vue.js фреймворк
- **Vuetify 3** - Material Design компоненты (с tree-shaking)
- **TypeScript** - Типизация
- **Pinia** - Управление состоянием

### Backend
- **FastAPI** - Python веб-фреймворк
- **SQLAlchemy** - ORM
- **Alembic** - Миграции БД
- **PostgreSQL** - База данных
- **JWT** - Аутентификация

## Структура проекта

```
sirius-web-lp-cursor/
├── frontend/          # Nuxt 4 приложение
│   ├── components/     # Vue компоненты
│   ├── pages/         # Страницы сайта
│   ├── layouts/       # Макеты
│   ├── composables/   # Композиции
│   ├── middleware/    # Middleware
│   └── public/        # Статические файлы
├── backend/           # FastAPI приложение
│   ├── app/
│   │   ├── api/       # API endpoints
│   │   ├── models/    # Модели БД
│   │   ├── schemas/   # Pydantic схемы
│   │   └── services/  # Бизнес-логика
│   └── migrations/    # Миграции Alembic
└── README.md
```

## Установка и запуск

### Backend

1. Создайте виртуальное окружение:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env`:
```env
DATABASE_URL=postgresql://postgres:Danil228@localhost:5440/sirius_db
SECRET_KEY=your-secret-key-change-in-production
API_BASE_URL=http://localhost:8009
```

4. База данных создастся автоматически при первом запуске!
   Или создайте вручную:
```bash
# Автоматическое создание БД и таблиц
python -m app.init_db

# Или используйте миграции Alembic (если настроены)
# alembic upgrade head
```

5. Создайте первого администратора:
```bash
python scripts/create_admin.py
```

6. Запустите сервер:
```bash
uvicorn app.main:app --reload --port 8009
# или
python run.py
```

**Примечание:** База данных и таблицы создадутся автоматически при первом запуске сервера!

### Frontend

1. Скопируйте изображения в папку `public`:
```bash
cd frontend/public
copy ..\..\logo.png .
copy ..\..\main-func.png .
```

2. Установите зависимости:
```bash
cd frontend
npm install
```

3. Создайте файл `.env`:
```env
API_BASE_URL=http://localhost:8009
```

4. Запустите dev сервер:
```bash
npm run dev
# Сервер будет доступен на http://localhost:3006
```

5. Соберите для production:
```bash
npm run build
npm run preview
```

## Основные функции

### Публичная часть
- Главная страница с hero секцией
- О компании
- Описание продукта ТГИД-07
- Возможности системы
- Отраслевые решения
- Контакты
- Форма заявки на демо
- Блог

### Админ-панель (CRM)
- Управление контентом (CRUD)
- SEO метатеги
- Управление заявками на демо
- Управление пользователями
- Аналитика

## API Endpoints

### Публичные
- `GET /api/pages/{slug}/content` - Получение контента страницы
- `POST /api/demo-requests` - Создание заявки на демо
- `POST /api/contact` - Отправка сообщения

### Защищенные (требуют авторизации)
- `POST /api/auth/login` - Вход
- `GET /api/auth/me` - Информация о текущем пользователе
- `GET /api/admin/content` - Список контента
- `POST /api/admin/content` - Создание контента
- `PUT /api/admin/content/{id}` - Обновление контента
- `DELETE /api/admin/content/{id}` - Удаление контента
- `GET /api/admin/demo-requests` - Список заявок
- `PUT /api/admin/demo-requests/{id}` - Обновление статуса заявки
- `GET /api/admin/analytics` - Аналитика

## SEO

- Open Graph метатеги
- Twitter Card метатеги
- WhatsApp preview
- Структурированные данные (JSON-LD)
- Sitemap.xml
- Robots.txt

## Адаптивность

Сайт полностью адаптивен для всех устройств:
- Mobile (xs, sm)
- Tablet (md)
- Desktop (lg, xl, xxl)

## Анимации

- Fade-in при загрузке
- Scroll animations (Intersection Observer)
- Hover эффекты
- Плавные переходы

## Домен и порты

- **Домен**: itwin.kz
- **Backend порт**: 8009
- **Frontend порт**: 3006
- **Nginx конфигурация**: см. `nginx/itwin.kz.conf`

## Production деплой

### Настройка Nginx

1. Скопируйте конфигурацию nginx:
```bash
sudo cp nginx/itwin.kz.conf /etc/nginx/sites-available/itwin.kz
sudo ln -s /etc/nginx/sites-available/itwin.kz /etc/nginx/sites-enabled/
```

2. Установите SSL сертификат:
```bash
sudo certbot --nginx -d itwin.kz -d www.itwin.kz
```

3. Перезагрузите nginx:
```bash
sudo systemctl reload nginx
```

### Systemd сервисы

Для автозапуска backend и frontend используйте systemd сервисы (см. `systemd/README.md`).

## Лицензия

Проприетарное программное обеспечение

