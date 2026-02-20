# Создание администратора

## Способ 1: Через скрипт (рекомендуется)

1. Активируйте виртуальное окружение:
```bash
cd backend
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac
```

2. Убедитесь, что установлены все зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите скрипт:
```bash
python create_admin_simple.py
```

4. Введите данные:
   - Email администратора
   - Пароль (будет скрыт при вводе)
   - Подтверждение пароля
   - ФИО администратора

## Способ 2: Через Python интерактивно

```python
from app.database import SessionLocal
from app.models.user import User
from app.services.auth import get_password_hash

db = SessionLocal()

admin = User(
    email="admin@itwin.kz",
    hashed_password=get_password_hash("ваш_пароль"),
    full_name="Администратор",
    is_superuser=True,
    is_active=True
)

db.add(admin)
db.commit()
print(f"Администратор создан: {admin.email}")
```

## Способ 3: Через API (после запуска сервера)

```bash
curl -X POST "http://localhost:8009/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@itwin.kz",
    "password": "ваш_пароль",
    "full_name": "Администратор"
  }'
```

Затем обновите пользователя через БД, установив `is_superuser=True`.

## Проверка

После создания администратора вы можете войти в систему:
- URL: http://localhost:3006/login
- Email: введенный email
- Пароль: введенный пароль

