# Nginx Configuration для itwin.kz

## Установка и настройка

### 1. Установка Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

### 2. Копирование конфигурации

```bash
# Скопируйте конфигурационный файл
sudo cp nginx/itwin.kz.conf /etc/nginx/sites-available/itwin.kz

# Создайте симлинк
sudo ln -s /etc/nginx/sites-available/itwin.kz /etc/nginx/sites-enabled/

# Удалите дефолтную конфигурацию (опционально)
sudo rm /etc/nginx/sites-enabled/default
```

### 3. Установка SSL сертификата (Let's Encrypt)

```bash
# Установите certbot
sudo apt install certbot python3-certbot-nginx

# Получите сертификат
sudo certbot --nginx -d itwin.kz -d www.itwin.kz

# Автоматическое обновление
sudo certbot renew --dry-run
```

### 4. Создание директорий

```bash
# Создайте директорию для логов
sudo mkdir -p /var/log/nginx/itwin.kz

# Создайте директорию для статических файлов (если нужно)
sudo mkdir -p /var/www/itwin.kz/public
```

### 5. Проверка конфигурации

```bash
# Проверьте синтаксис
sudo nginx -t

# Перезагрузите Nginx
sudo systemctl reload nginx
# или
sudo service nginx reload
```

### 6. Настройка firewall

```bash
# Разрешите HTTP и HTTPS
sudo ufw allow 'Nginx Full'
# или
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## Структура

- **Backend API**: проксируется на `http://127.0.0.1:8009` через `/api/`
- **Frontend SSR**: проксируется на `http://127.0.0.1:3006` через `/`

## Важные замечания

1. **SSL сертификаты**: Обновите пути к сертификатам в конфигурации после установки
2. **Порты**: Убедитесь, что backend (8009) и frontend (3006) запущены
3. **DNS**: Настройте A-запись для домена itwin.kz на IP вашего сервера
4. **Логи**: Проверяйте логи при проблемах: `/var/log/nginx/itwin.kz.error.log`

## Тестирование

После настройки проверьте:
- HTTP редирект на HTTPS: `http://itwin.kz`
- HTTPS доступ: `https://itwin.kz`
- API endpoints: `https://itwin.kz/api/health`
- Frontend: `https://itwin.kz`

## Troubleshooting

### Проблемы с подключением
```bash
# Проверьте статус Nginx
sudo systemctl status nginx

# Проверьте логи
sudo tail -f /var/log/nginx/itwin.kz.error.log
```

### Проблемы с SSL
```bash
# Проверьте сертификат
sudo certbot certificates

# Обновите сертификат вручную
sudo certbot renew
```

### Перезапуск сервисов
```bash
# Перезапуск Nginx
sudo systemctl restart nginx

# Перезапуск backend (если используется systemd)
sudo systemctl restart sirius-backend

# Перезапуск frontend (если используется systemd)
sudo systemctl restart sirius-frontend
```

