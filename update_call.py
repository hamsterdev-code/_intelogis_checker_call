"""
Скрипт для ручного обновления данных звонка через API
Позволяет вводить ID звонка и критерии через input
"""

import requests
import json
from config import (
    API_POST_RESULTS,
    API_AUTH_TOKEN,
    API_COOKIE_DDG1,
    API_COOKIE_JWT_CHECK,
    API_COOKIE_PHPSESSID,
    API_REQUEST_TIMEOUT
)


def setup_session():
    """
    Настраивает сессию с авторизацией
    """
    session = requests.Session()
    
    # Устанавливаем заголовки
    session.headers.update({
        'Authorization': f'Bearer {API_AUTH_TOKEN}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://dl-ils.intelogis.ru',
        'referer': 'https://dl-ils.intelogis.ru/',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    })
    
    # Устанавливаем cookies
    session.cookies.update({
        '__ddg1_': API_COOKIE_DDG1,
        'jwtCheck6925a697e90a5': API_COOKIE_JWT_CHECK,
        'PHPSESSID': API_COOKIE_PHPSESSID,
    })
    
    return session


def send_result_to_api(session, call_id, criteria_1, criteria_2, criteria_3, criteria_4, text=""):
    """
    Отправляет результат анализа в API
    POST /callsAnalyze/result
    
    Args:
        session: requests.Session с авторизацией
        call_id: ID звонка
        criteria_1: Значение критерия 1 (0.0 или 1.0)
        criteria_2: Значение критерия 2 (0.0 или 1.0)
        criteria_3: Значение критерия 3 (0.0 до 1.0)
        criteria_4: Значение критерия 4 (0.0 или 1.0)
        text: Текст транскрипции (опционально)
    """
    # Формируем результат в том же формате, что и в server.py
    result = {
        'id': call_id,
        'text': text,
        'criteria': [
            {'tag': 1, 'value': float(criteria_1)},
            {'tag': 2, 'value': float(criteria_2)},
            {'tag': 3, 'value': float(criteria_3)},
            {'tag': 4, 'value': float(criteria_4)},
        ]
    }
    
    print(f"\nОтправка данных для звонка ID: {call_id}")
    print(f"Критерии:")
    print(f"  - Критерий 1: {criteria_1}")
    print(f"  - Критерий 2: {criteria_2}")
    print(f"  - Критерий 3: {criteria_3}")
    print(f"  - Критерий 4: {criteria_4}")
    if text:
        print(f"Текст: {text[:100]}..." if len(text) > 100 else f"Текст: {text}")
    
    try:
        response = session.post(
            API_POST_RESULTS,
            json=result,
            timeout=API_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        
        print(f"✅ Успешно отправлено! HTTP {response.status_code}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Ошибка HTTP: {e}")
        if hasattr(e.response, 'text'):
            print(f"   Ответ сервера: {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return False


def get_float_input(prompt, min_value=0.0, max_value=1.0, default=None):
    """
    Получает float значение от пользователя с валидацией
    
    Args:
        prompt: Текст запроса
        min_value: Минимальное значение
        max_value: Максимальное значение
        default: Значение по умолчанию (если Enter без ввода)
    """
    while True:
        if default is not None:
            user_input = input(f"{prompt} (по умолчанию: {default}): ").strip()
            if not user_input:
                return default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        try:
            value = float(user_input)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"⚠️ Значение должно быть от {min_value} до {max_value}")
        except ValueError:
            print("⚠️ Введите корректное число")


def main():
    """
    Главная функция - интерактивное обновление данных звонка
    """
    print("=" * 60)
    print("ОБНОВЛЕНИЕ ДАННЫХ ЗВОНКА")
    print("=" * 60)
    print()
    
    # Настраиваем сессию
    session = setup_session()
    
    while True:
        try:
            # Запрашиваем ID звонка
            call_id_input = input("\nВведите ID звонка (или 'q' для выхода): ").strip()
            
            if call_id_input.lower() == 'q':
                print("Выход...")
                break
            
            try:
                call_id = int(call_id_input)
            except ValueError:
                print("⚠️ ID должен быть числом")
                continue
            
            # Запрашиваем критерии
            print("\nВведите значения критериев:")
            print("  Критерий 1 (call_was_made): 0.0 или 1.0")
            print("  Критерий 2 (work_related): 0.0 или 1.0")
            print("  Критерий 3 (script_compliance): от 0.0 до 1.0")
            print("  Критерий 4 (positive_outcome): 0.0 или 1.0")
            print()
            
            criteria_1 = get_float_input("Критерий 1", min_value=0.0, max_value=1.0)
            criteria_2 = get_float_input("Критерий 2", min_value=0.0, max_value=1.0)
            criteria_3 = get_float_input("Критерий 3", min_value=0.0, max_value=1.0)
            criteria_4 = get_float_input("Критерий 4", min_value=0.0, max_value=1.0)
            
            # Опционально: текст транскрипции
            text_input = input("\nВведите текст транскрипции (Enter для пропуска): ").strip()
            text = text_input if text_input else ""
            
            # Отправляем данные
            success = send_result_to_api(
                session,
                call_id,
                criteria_1,
                criteria_2,
                criteria_3,
                criteria_4,
                text
            )
            
            if success:
                print("\n✅ Данные успешно обновлены!")
            else:
                print("\n❌ Ошибка при обновлении данных")
            
            # Спрашиваем, хотим ли продолжить
            continue_input = input("\nОбновить еще один звонок? (y/n): ").strip().lower()
            if continue_input != 'y':
                break
                
        except KeyboardInterrupt:
            print("\n\nВыход...")
            break
        except Exception as e:
            print(f"\n❌ Неожиданная ошибка: {e}")
            continue_input = input("\nПродолжить? (y/n): ").strip().lower()
            if continue_input != 'y':
                break
    
    print("\n" + "=" * 60)
    print("Работа завершена")
    print("=" * 60)


if __name__ == "__main__":
    main()

