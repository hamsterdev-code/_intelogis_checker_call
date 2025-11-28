"""
Конфигурация для сервера анализа звонков
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# ==================== API НАСТРОЙКИ ====================

# Базовый URL API (укажите ваш реальный API)
API_BASE_URL = os.getenv("API_BASE_URL", "https://saas.intelogis.ru/digitalLogistILS")

# Endpoints
API_GET_CALLS = f"{API_BASE_URL}/callsAnalyze"
API_POST_RESULTS = f"{API_BASE_URL}/callsAnalyze/result"

# Количество звонков для обработки за раз
CALLS_COUNT = int(os.getenv("CALLS_COUNT", "10"))

# ==================== АВТОРИЗАЦИЯ ====================

# Bearer Token для авторизации
API_AUTH_TOKEN = os.getenv(
    "API_AUTH_TOKEN",
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE3NjQwNzUxNTksImlzcyI6InNhYXMuaW50ZWxvZ2lzLnJ1IiwiYXVkIjoic2Fhcy5pbnRlbG9naXMucnUiLCJuYmYiOjE3NjQwNzUxNTksImV4cCI6MTc2NDY3OTk1OSwianRpIjoiUDNob1ZaNEZhanNXUU1pNUx6ZVNERTgyIiwidXNlcklkIjoiNTE0NSIsImFjY291bnRJZCI6Ijg1NyIsImhhc2giOiI2OTI1YTY5N2U5MGE1In0.QbDmLSDmJLpw2ZLkR3g1rgxqW4D1lQCwqKEvwHdYXajhUXrd0hF2RoI7cTlka8lF1sFbD0JqKcEGwtWW7vTSrw"
)

# Cookies для авторизации
API_COOKIE_DDG1 = os.getenv(
    "API_COOKIE_DDG1",
    "svV1LyxcAuTUttiPEG05"
)

API_COOKIE_JWT_CHECK = os.getenv(
    "API_COOKIE_JWT_CHECK",
    "P3hoVZ4FajsWQMi5LzeSDE82"
)

API_COOKIE_PHPSESSID = os.getenv(
    "API_COOKIE_PHPSESSID",
    "ksaaks5sf3mn596r9dufhfkr03hu3cb4q0b22qdl78pm23ch"
)

# ==================== OPENAI НАСТРОЙКИ ====================

# OpenRouter API Key
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "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"
)

# OpenRouter базовый URL
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

# Модель для анализа
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini")

# ==================== WHISPER НАСТРОЙКИ ====================

# Размер модели Whisper: tiny, base, small, medium, large, large-v2, large-v3
# Рекомендуется: base для баланса скорости и качества
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "medium")

# Язык распознавания
WHISPER_LANGUAGE = "ru"

# Устройство для обработки: "cpu", "cuda" (GPU), "auto" (автоматический выбор)
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "auto")

# Количество потоков для CPU (0 = автоматически)
WHISPER_CPU_THREADS = int(os.getenv("WHISPER_CPU_THREADS", "0"))

# Размер луча для поиска (меньше = быстрее, но может быть менее точно)
# Рекомендуется: 1-2 для скорости, 5 для качества
WHISPER_BEAM_SIZE = int(os.getenv("WHISPER_BEAM_SIZE", "2"))

# ==================== ПУТИ И ДИРЕКТОРИИ ====================

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Директория для временных аудиофайлов
TEMP_DIRECTORY = BASE_DIR / "temp_audio"
TEMP_DIRECTORY.mkdir(exist_ok=True)

# База данных
DATABASE_PATH = BASE_DIR / "calls_database.db"

# Лог файл
LOG_FILE = BASE_DIR / "calls_analyzer.log"

# ==================== РАСПИСАНИЕ ====================

# Интервал запуска задачи (в часах)
SCHEDULE_INTERVAL_HOURS = int(os.getenv("SCHEDULE_INTERVAL_HOURS", "1"))

# Запускать ли задачу сразу при старте (для тестирования)
RUN_ON_STARTUP = os.getenv("RUN_ON_STARTUP", "true").lower() == "true"

# ==================== ТАЙМАУТЫ ====================

# Таймаут для скачивания аудио (секунды)
AUDIO_DOWNLOAD_TIMEOUT = int(os.getenv("AUDIO_DOWNLOAD_TIMEOUT", "60"))

# Таймаут для API запросов (секунды)
API_REQUEST_TIMEOUT = int(os.getenv("API_REQUEST_TIMEOUT", "30"))

# Пауза между отправкой результатов (секунды)
SEND_RESULTS_DELAY = int(os.getenv("SEND_RESULTS_DELAY", "1"))

# ==================== ЛОГИРОВАНИЕ ====================

# Уровень логирования для консоли: DEBUG, INFO, WARNING, ERROR
CONSOLE_LOG_LEVEL = os.getenv("CONSOLE_LOG_LEVEL", "INFO")

# Уровень логирования для файла
FILE_LOG_LEVEL = os.getenv("FILE_LOG_LEVEL", "DEBUG")

# Логировать ли распознанный текст из аудио
LOG_TRANSCRIBED_TEXT = os.getenv("LOG_TRANSCRIBED_TEXT", "true").lower() == "true"

# Максимальный размер лог файла (байты) - 10MB по умолчанию
LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))

# Количество ротируемых лог файлов
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))


def print_config():
    """Выводит текущую конфигурацию"""
    print("="*80)
    print("КОНФИГУРАЦИЯ СЕРВЕРА")
    print("="*80)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Количество звонков: {CALLS_COUNT}")
    print(f"Интервал запуска: каждые {SCHEDULE_INTERVAL_HOURS} час(а)")
    print(f"Запуск при старте: {RUN_ON_STARTUP}")
    print(f"Модель Whisper: {WHISPER_MODEL_SIZE}")
    print(f"Модель OpenAI: {OPENAI_MODEL}")
    print(f"База данных: {DATABASE_PATH}")
    print(f"Лог файл: {LOG_FILE}")
    print(f"Временная директория: {TEMP_DIRECTORY}")
    print("="*80)


if __name__ == "__main__":
    print_config()

