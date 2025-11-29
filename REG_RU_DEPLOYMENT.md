# Инструкция по установке на VPS REG.RU

## Выбор операционной системы

**Рекомендуется: Ubuntu 22.04 LTS** (Long Term Support)

### Почему Ubuntu 22.04 LTS?

✅ **Стабильность** - LTS версия с поддержкой до 2027 года  
✅ **Совместимость** - отлично работает с Python 3.11 и PyTorch  
✅ **Документация** - огромное количество руководств и примеров  
✅ **Пакеты** - все необходимые библиотеки доступны из репозиториев  
✅ **Простота** - легко настроить даже новичку  

### Альтернативные варианты:

1. **Ubuntu 24.04 LTS** - новее, но может быть менее стабильной
2. **Debian 12 (Bookworm)** - легковесная, стабильная, но меньше документации
3. **Debian 11 (Bullseye)** - очень стабильная, но старее

### Не рекомендуется:

❌ **CentOS/Rocky Linux** - сложнее с Python пакетами  
❌ **Windows Server** - не подходит для Python-скриптов  
❌ **Alpine Linux** - слишком минималистичная, проблемы с компиляцией  

### При заказе VPS в REG.RU:

Выберите **Ubuntu 22.04 LTS** в настройках при создании сервера.

---

## Шаг 1: Подключение к серверу

### Получение данных для подключения

1. Войдите в панель управления REG.RU
2. Перейдите в раздел "VPS"
3. Найдите ваш сервер и скопируйте:
   - **IP-адрес** сервера
   - **Логин** (обычно `root`)
   - **Пароль** (или используйте SSH-ключ)

### Подключение по SSH

**Windows:**
- Используйте **PuTTY** (скачать: https://www.putty.org/)
- Или используйте **Windows Terminal** / **PowerShell**:
  ```powershell
  ssh root@ваш_IP_адрес
  ```

**Linux/Mac:**
```bash
ssh root@ваш_IP_адрес
```

При первом подключении подтвердите добавление сервера в список известных хостов (введите `yes`).

## Шаг 2: Обновление системы

```bash
# Обновление списка пакетов
apt update && apt upgrade -y

# Установка необходимых системных пакетов
apt install -y python3.11 python3.11-venv python3-pip ffmpeg git curl wget
```

**Проверка установки:**
```bash
python3 --version  # Должно показать Python 3.11.x
ffmpeg -version    # Проверка ffmpeg
```

## Шаг 3: Создание пользователя для приложения

```bash
# Создаем пользователя (без пароля, только для запуска приложения)
adduser --disabled-password --gecos "" checker

# Создаем директорию для приложения
mkdir -p /home/checker/app
chown checker:checker /home/checker/app
```

## Шаг 4: Загрузка файлов на сервер

### Вариант А: Через SCP (из Windows PowerShell или Linux/Mac)

```bash
# Перейдите в папку с вашими файлами на локальном компьютере
cd путь/к/вашей/папке/с/проектом

# Загрузите файлы на сервер
scp server.py root@ваш_IP_адрес:/home/checker/app/
scp config.py root@ваш_IP_адрес:/home/checker/app/
scp scripts.txt root@ваш_IP_адрес:/home/checker/app/
scp requirements.txt root@ваш_IP_адрес:/home/checker/app/
```

### Вариант Б: Через WinSCP (Windows)

1. Скачайте WinSCP: https://winscp.net/
2. Подключитесь к серверу
3. Перетащите файлы в `/home/checker/app/`

### Вариант В: Через Git (если код в репозитории)

```bash
# На сервере
cd /home/checker/app
git clone ваш_репозиторий .
```

## Шаг 5: Установка зависимостей

### ⚠️ ВАЖНО: Всегда используйте виртуальное окружение!

**НЕ устанавливайте пакеты в системный Python** - это вызовет ошибку "externally-managed-environment".

```bash
# Переключаемся на пользователя checker
su - checker
cd /home/checker/app

# Создаем виртуальное окружение
# Используйте python3 (будет использована доступная версия: 3.11 или 3.12)
python3 -m venv venv

# Активируем виртуальное окружение
# Обратите внимание: после активации в начале строки появится (venv)
source venv/bin/activate

# Проверьте, что виртуальное окружение активно:
# Команда which python должна показать путь к venv
which python

# Обновляем pip
pip install --upgrade pip

# Устанавливаем PyTorch (CPU версия)
# Теперь pip будет работать, так как виртуальное окружение активно
pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Устанавливаем остальные зависимости
pip install --no-cache-dir -r requirements.txt
```

**Проверка установки:**
```bash
# Убедитесь, что виртуальное окружение активно (должно быть (venv) в начале строки)
python -c "import torch; import whisper; print('✅ Все зависимости установлены')"
```

**Если вышли из виртуального окружения**, активируйте его снова:
```bash
cd /home/checker/app
source venv/bin/activate
```

## Шаг 6: Настройка конфигурации

Убедитесь, что файл `config.py` настроен правильно:

```bash
nano /home/checker/app/config.py
```

Проверьте пути:
- `DATABASE_PATH` - должен быть доступен для записи
- `LOG_FILE` - должен быть доступен для записи
- `TEMP_DIRECTORY` - должен существовать

## Шаг 7: Создание необходимых директорий

```bash
# Создаем директории для логов и временных файлов
mkdir -p /home/checker/app/logs
mkdir -p /home/checker/app/temp_audio

# Устанавливаем права доступа
chown -R checker:checker /home/checker/app
chmod -R 755 /home/checker/app
```

## Шаг 8: Настройка systemd сервиса

Выйдите из пользователя checker (нажмите `Ctrl+D` или введите `exit`), затем создайте сервис:

```bash
# Создаем файл сервиса
nano /etc/systemd/system/calls-checker.service
```

**Вставьте следующее содержимое:**

```ini
[Unit]
Description=Calls Checker Worker
After=network.target

[Service]
Type=simple
User=checker
Group=checker
WorkingDirectory=/home/checker/app
Environment="PATH=/home/checker/app/venv/bin"
ExecStart=/home/checker/app/venv/bin/python /home/checker/app/server.py
Restart=always
RestartSec=10
StandardOutput=append:/home/checker/app/logs/service.log
StandardError=append:/home/checker/app/logs/service_error.log

# Ограничения ресурсов (опционально, раскомментируйте при необходимости)
# MemoryLimit=4G
# CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

**Сохраните файл:** `Ctrl+O`, затем `Enter`, затем `Ctrl+X`

## Шаг 9: Запуск сервиса

```bash
# Перезагружаем конфигурацию systemd
systemctl daemon-reload

# Включаем автозапуск при загрузке системы
systemctl enable calls-checker

# Запускаем сервис
systemctl start calls-checker

# Проверяем статус
systemctl status calls-checker
```

## Шаг 10: Проверка работы

### Просмотр логов

```bash
# Логи systemd
journalctl -u calls-checker -f

# Логи приложения
tail -f /home/checker/app/calls_analyzer.log

# Логи сервиса
tail -f /home/checker/app/logs/service.log
```

### Проверка процесса

```bash
# Проверка, что процесс запущен
ps aux | grep server.py

# Проверка использования ресурсов
htop
# или
top
```

## Управление сервисом

```bash
# Остановить
systemctl stop calls-checker

# Запустить
systemctl start calls-checker

# Перезапустить
systemctl restart calls-checker

# Посмотреть статус
systemctl status calls-checker

# Отключить автозапуск
systemctl disable calls-checker
```

## Решение проблем

### Проблема: Сервис не запускается

```bash
# Проверьте логи ошибок
journalctl -u calls-checker -n 50 --no-pager

# Проверьте права доступа
ls -la /home/checker/app
chown -R checker:checker /home/checker/app

# Проверьте, что виртуальное окружение активировано правильно
/home/checker/app/venv/bin/python --version
```

### Проблема: Нехватка памяти

Если модель Whisper не загружается из-за нехватки памяти:

1. **Используйте модель меньшего размера** в `config.py`:
   ```python
   WHISPER_MODEL_SIZE = "base"  # вместо "medium"
   ```

2. **Добавьте swap файл:**
   ```bash
   # Создаем swap файл 2GB
   fallocate -l 2G /swapfile
   chmod 600 /swapfile
   mkswap /swapfile
   swapon /swapfile
   
   # Делаем постоянным
   echo '/swapfile none swap sw 0 0' >> /etc/fstab
   ```

### Проблема: Модель не скачивается

```bash
# Проверьте интернет-соединение
ping google.com

# Попробуйте скачать модель вручную
cd /home/checker/app
source venv/bin/activate
python -c "import whisper; whisper.load_model('base')"
```

### Проблема: Ошибки прав доступа

```bash
# Установите правильные права
chown -R checker:checker /home/checker/app
chmod -R 755 /home/checker/app
chmod +x /home/checker/app/server.py
```

## Обновление кода

```bash
# Остановите сервис
systemctl stop calls-checker

# Загрузите новые файлы (через scp, git pull и т.д.)
cd /home/checker/app
# ... загрузите новые файлы ...

# Если изменились зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запустите сервис
systemctl start calls-checker
```

## Мониторинг

### Проверка использования ресурсов

```bash
# CPU и память
htop

# Диск
df -h

# Сетевые подключения
netstat -tulpn | grep python
```

### Настройка мониторинга (опционально)

Можно настроить отправку уведомлений при ошибках через email или Telegram бота (добавить в код).

## Безопасность

### Настройка firewall

```bash
# Установка ufw (если не установлен)
apt install ufw -y

# Разрешаем SSH
ufw allow 22/tcp

# Включаем firewall
ufw enable

# Проверка статуса
ufw status
```

### Отключение входа по паролю (рекомендуется)

Настройте вход только по SSH-ключу для повышения безопасности.

## Контакты поддержки REG.RU

Если возникли проблемы с VPS:
- Техподдержка: https://www.reg.ru/support/
- Документация: https://help.reg.ru/

## Дополнительные ресурсы

- [Официальная документация REG.RU по VPS](https://help.reg.ru/support/hosting/vps)
- [Установка Flask на VPS REG.RU](https://help.reg.ru/support/hosting/php-asp-net-i-skripty/kak-ustanovit-flask-na-hosting)

---

**Готово!** Ваш скрипт должен работать на VPS REG.RU. Проверьте логи, чтобы убедиться, что все работает корректно.

