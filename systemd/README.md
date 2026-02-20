# Systemd Service Files

Файлы для запуска backend и frontend как системных сервисов.

## Установка

### Backend Service

1. Отредактируйте пути в файле `sirius-backend.service`:
   - `WorkingDirectory` - путь к директории backend
   - `Environment PATH` - путь к виртуальному окружению
   - `EnvironmentFile` - путь к .env файлу
   - `ExecStart` - путь к uvicorn

2. Скопируйте файл:
```bash
sudo cp systemd/sirius-backend.service /etc/systemd/system/
```

3. Перезагрузите systemd:
```bash
sudo systemctl daemon-reload
```

4. Включите автозапуск:
```bash
sudo systemctl enable sirius-backend
```

5. Запустите сервис:
```bash
sudo systemctl start sirius-backend
```

6. Проверьте статус:
```bash
sudo systemctl status sirius-backend
```

### Frontend Service

1. Отредактируйте пути в файле `sirius-frontend.service`:
   - `WorkingDirectory` - путь к директории frontend
   - `ExecStart` - путь к скомпилированному приложению

2. Скопируйте файл:
```bash
sudo cp systemd/sirius-frontend.service /etc/systemd/system/
```

3. Перезагрузите systemd:
```bash
sudo systemctl daemon-reload
```

4. Включите автозапуск:
```bash
sudo systemctl enable sirius-frontend
```

5. Запустите сервис:
```bash
sudo systemctl start sirius-frontend
```

6. Проверьте статус:
```bash
sudo systemctl status sirius-frontend
```

## Управление сервисами

```bash
# Остановить
sudo systemctl stop sirius-backend
sudo systemctl stop sirius-frontend

# Запустить
sudo systemctl start sirius-backend
sudo systemctl start sirius-frontend

# Перезапустить
sudo systemctl restart sirius-backend
sudo systemctl restart sirius-frontend

# Просмотр логов
sudo journalctl -u sirius-backend -f
sudo journalctl -u sirius-frontend -f
```

## Важные замечания

1. Убедитесь, что виртуальное окружение Python активировано в PATH
2. Убедитесь, что frontend собран (`npm run build`)
3. Проверьте права доступа к файлам и директориям
4. Убедитесь, что порты 8009 и 3006 не заняты другими процессами

