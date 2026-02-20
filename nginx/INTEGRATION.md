# Интеграция проекта Сириус в существующую конфигурацию nginx

## Варианты размещения

### Вариант 1: Отдельный путь `/sirius/` (РЕКОМЕНДУЕТСЯ)

Если корневой путь `/` уже занят другим проектом, используйте отдельный путь:

**Доступ:**
- Frontend: `https://itwin.kz/sirius/`
- Backend API: `https://itwin.kz/api-sirius/`

**Преимущества:**
- Не конфликтует с существующими проектами
- Легко переключаться между проектами
- Можно использовать несколько проектов одновременно

**Недостатки:**
- Нужно обновить конфигурацию Nuxt для работы с базовым путем `/sirius/`

### Вариант 2: Корневой путь `/` (если нужно заменить текущий проект)

Если хотите сделать Сириус основным проектом на домене:

**Доступ:**
- Frontend: `https://itwin.kz/`
- Backend API: `https://itwin.kz/api/` или `/api-sirius/`

**ВНИМАНИЕ:** Это заменит текущий проект на порту 3001!

## Инструкция по добавлению

### Шаг 1: Добавьте блоки в конфигурацию

Откройте ваш файл конфигурации nginx и добавьте следующие блоки **ПЕРЕД** другими location блоками (или в нужном месте по приоритету):

```nginx
# Backend API для Сириус
location /api-sirius/ {
	client_max_body_size 50M;
    proxy_pass http://localhost:8009/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
	
	proxy_http_version 1.1;
	proxy_set_header Upgrade $http_upgrade;
	proxy_set_header Connection "upgrade";
	proxy_read_timeout 300s;
	proxy_connect_timeout 75s;
}

# Frontend для Сириус (вариант с отдельным путем)
location /sirius/ {
    proxy_pass http://localhost:3006/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Port $server_port;
	
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}
```

### Шаг 2: Обновите конфигурацию Nuxt (если используете `/sirius/`)

Если выбрали вариант с отдельным путем, обновите `frontend/nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  // ... другие настройки
  
  app: {
    baseURL: '/sirius/', // Добавьте базовый путь
    // ... остальные настройки
  },
  
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'https://itwin.kz/api-sirius'
    }
  }
})
```

### Шаг 3: Обновите конфигурацию Backend

Убедитесь, что CORS настроен правильно в `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3006",
        "https://itwin.kz",
        "http://itwin.kz"
    ],
    # ...
)
```

### Шаг 4: Проверьте конфигурацию и перезагрузите nginx

```bash
# Проверка синтаксиса
nginx -t

# Перезагрузка (Windows)
nginx -s reload

# Или перезапуск сервиса (Windows)
net stop nginx
net start nginx
```

## Проверка работы

После настройки проверьте:

1. **Backend API:**
   ```bash
   curl https://itwin.kz/api-sirius/health
   ```

2. **Frontend:**
   - Откройте в браузере: `https://itwin.kz/sirius/` (если используете отдельный путь)
   - Или: `https://itwin.kz/` (если используете корневой путь)

3. **API документация:**
   - `https://itwin.kz/api-sirius/docs`

## Приоритет location блоков

Nginx обрабатывает location блоки в следующем порядке:
1. Точные совпадения (`=`)
2. Префиксы с `^~`
3. Обычные префиксы (по длине)
4. Регулярные выражения

Убедитесь, что блоки для Сириус добавлены в правильном месте, чтобы не конфликтовать с другими проектами.

## Troubleshooting

### Проблема: 404 ошибка

- Проверьте, что backend и frontend запущены на правильных портах (8009 и 3006)
- Проверьте логи nginx: `error.log`
- Убедитесь, что пути в конфигурации правильные

### Проблема: CORS ошибки

- Проверьте настройки CORS в backend
- Убедитесь, что домен добавлен в `allow_origins`

### Проблема: WebSocket не работает

- Убедитесь, что добавлены заголовки `Upgrade` и `Connection`
- Проверьте таймауты `proxy_read_timeout`

