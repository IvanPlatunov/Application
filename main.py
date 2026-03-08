#!/usr/bin/env python3
"""
Точка входа приложения.
Запускает HTTP-сервер с контроллером.
"""

import os
import sys
from controllers.server_controller import create_server
# Добавляем текущую директорию в путь Python для корректных импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def main():
    """Основная функция запуска приложения."""
    
    # Создаем и запускаем сервер
    host = 'localhost'
    port = 8080
    
    print(f"\n{'='*60}")
    print("Запуск сервера приложения")
    print(f"{'='*60}")
    print(f"Рабочая директория: {os.getcwd()}")
    print(f"Сервер будет доступен по адресу: http://{host}:{port}")
    print(f"\nДоступные страницы:")
    print("  /                       - Главная страница")
    print("  /currencies            - Список валют")
    print("  /users                 - Список пользователей")
    print("  /api/currencies        - API валют (JSON)")
    print("  /api/subscriptions     - API подписок (JSON)")
    print("  POST /api/subscribe    - Добавить подписку")
    print("  POST /api/update_currencies - Обновить курсы валют")
    print(f"\n{'='*60}")
    print("Нажмите Ctrl+C для остановки сервера")
    print(f"{'='*60}\n")
    
    try:
        create_server()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"\nОшибка при запуске сервера: {e}")
        print("Проверьте:")
        print("1. Порт 8080 не занят другим приложением")
        print("2. Все зависимости установлены (pip install jinja2 requests)")
        print("3. Структура папок создана правильно")


if __name__ == '__main__':
    main()