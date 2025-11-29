# Руководство по развертыванию на VPS

## Рекомендуемые хостинги

### 1. **DigitalOcean** (рекомендуется)
- **Цена**: от $4/мес (1GB RAM, 1 vCPU)
- **Плюсы**: Простой интерфейс, хорошая документация, быстрая поддержка
- **Ссылка**: https://www.digitalocean.com/
- **Минимум**: Droplet с 2GB RAM для модели Whisper medium

### 2. **Hetzner** (лучшее соотношение цена/качество)
- **Цена**: от €4.51/мес (2GB RAM, 1 vCPU)
- **Плюсы**: Немецкое качество, хорошая производительность, дешевле конкурентов
- **Ссылка**: https://www.hetzner.com/cloud
- **Минимум**: CX11 (2GB RAM)

### 3. **Vultr**
- **Цена**: от $2.50/мес (512MB RAM) или $6/мес (1GB RAM)
- **Плюсы**: Быстрые SSD, много локаций
- **Ссылка**: https://www.vultr.com/
- **Минимум**: 2GB RAM

### 4. **Linode (Akamai)**
- **Цена**: от $5/мес (1GB RAM)
- **Плюсы**: Стабильность, хорошая производительность
- **Ссылка**: https://www.linode.com/

### 5. **Scaleway**
- **Цена**: от €3.99/мес (2GB RAM)
- **Плюсы**: Европейские датацентры, хорошая цена
- **Ссылка**: https://www.scaleway.com/

## Минимальные требования

- **RAM**: 2GB (рекомендуется 4GB для модели Whisper medium)
- **CPU**: 1 vCPU (рекомендуется 2 vCPU)
- **Диск**: 20GB SSD
- **ОС**: Ubuntu 22.04 LTS или Debian 11/12

## Установка на VPS

### Шаг 1: Подключение к серверу

```bash
ssh root@your-server-ip
```

### Шаг 2: Обновление системы

```bash
apt update && apt upgrade -y
```

### Шаг 3: Установка Python и зависимостей

```bash
apt install -y python3.11 python3.11-venv python3-pip ffmpeg git
```

### Шаг 4: Создание пользователя для приложения

```bash
adduser --disabled-password --gecos "" checker
mkdir -p /home/checker/app
chown checker:checker /home/checker/app
```

### Шаг 5: Загрузка кода

```bash
cd /home/checker/app
# Загрузите файлы через git или scp:
# - server_simple.py
# - config.py
# - scripts.txt
# - requirements.txt
```

### Шаг 6: Установка зависимостей

```bash
cd /home/checker/app
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Шаг 7: Настройка systemd service

Создайте файл `/etc/systemd/system/calls-checker.service`:

```ini
[Unit]
Description=Calls Checker Worker
After=network.target

[Service]
Type=simple
User=checker
WorkingDirectory=/home/checker/app
Environment="PATH=/home/checker/app/venv/bin"
ExecStart=/home/checker/app/venv/bin/python /home/checker/app/server_simple.py
Restart=always
RestartSec=10
StandardOutput=append:/home/checker/app/logs/service.log
StandardError=append:/home/checker/app/logs/service_error.log

[Install]
WantedBy=multi-user.target
```

### Шаг 8: Создание директорий и настройка прав

```bash
mkdir -p /home/checker/app/logs
mkdir -p /home/checker/app/temp_audio
chown -R checker:checker /home/checker/app
```

### Шаг 9: Запуск сервиса

```bash
systemctl daemon-reload
systemctl enable calls-checker
systemctl start calls-checker
```

### Шаг 10: Проверка статуса

```bash
systemctl status calls-checker
tail -f /home/checker/app/logs/service.log
```

## Управление сервисом

```bash
# Остановить
systemctl stop calls-checker

# Запустить
systemctl start calls-checker

# Перезапустить
systemctl restart calls-checker

# Посмотреть логи
journalctl -u calls-checker -f
tail -f /home/checker/app/calls_analyzer.log
```

## Альтернатива: Запуск через screen/tmux

Если не хотите использовать systemd:

```bash
# Установка screen
apt install screen -y

# Создание сессии
screen -S checker

# Запуск в сессии
cd /home/checker/app
source venv/bin/activate
python server_simple.py

# Отключиться: Ctrl+A, затем D
# Вернуться: screen -r checker
```

## Мониторинг

### Проверка использования ресурсов

```bash
# CPU и память
htop

# Диск
df -h

# Логи приложения
tail -f /home/checker/app/calls_analyzer.log
```

### Автоматический перезапуск при сбое

Systemd автоматически перезапустит сервис при сбое (благодаря `Restart=always`).

## Обновление кода

```bash
cd /home/checker/app
systemctl stop calls-checker
# Загрузите новые файлы
systemctl start calls-checker
```

## Рекомендации по безопасности

1. Настройте firewall (ufw):
```bash
ufw allow 22/tcp
ufw enable
```

2. Используйте SSH ключи вместо паролей

3. Регулярно обновляйте систему:
```bash
apt update && apt upgrade -y
```

## Troubleshooting

### Проблема: Процесс не запускается

```bash
# Проверьте логи
journalctl -u calls-checker -n 50
tail -f /home/checker/app/calls_analyzer.log

# Проверьте права доступа
ls -la /home/checker/app
```

### Проблема: Нехватка памяти

- Используйте модель Whisper `base` вместо `medium`
- Увеличьте RAM на сервере
- Добавьте swap файл:

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Проблема: Модель не загружается

- Проверьте интернет-соединение
- Убедитесь, что есть достаточно места на диске
- Попробуйте использовать модель `base` вместо `medium`

