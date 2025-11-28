# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
# Сначала устанавливаем PyTorch (CPU версия для стабильности)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Копируем файлы приложения (кроме тех, что в .dockerignore)
COPY config.py server.py scripts.txt ./

# Создаем необходимые директории
RUN mkdir -p temp_audio backup_logs

# Устанавливаем переменные окружения для PyTorch (отключение проблемных оптимизаций)
ENV MKLDNN_VERBOSE=0
ENV MKL_VERBOSE=0
ENV TORCH_ALLOW_TF32_CUBLAS_OVERRIDE=0
ENV ONEDNN_VERBOSE=0
ENV MKLDNN_ENABLED=0
ENV USE_NNPACK=0
ENV PYTORCH_DISABLE_NNPACK=1
ENV PYTORCH_NNPACK_DISABLED=1

# Открываем порт (если нужно для мониторинга, хотя приложение не веб-сервер)
# EXPOSE 8000

# Запускаем приложение
CMD ["python", "server.py"]

