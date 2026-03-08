"""
Модуль контроллеров приложения.
Содержит HTTP-обработчики и логику создания сервера.
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader

# Импорты моделей
from models.author import Author
from models.app import App
from models.user import User
from models.currency import Currency
from models.user_currency import UserCurrency

# Импорт сервисов
from services.currency_service import CurrencyService


class ApplicationHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP-запросов приложения."""
    
    def do_GET(self):
        """Обработка GET запросов."""
        path = urlparse(self.path).path
        
        if path == '/':
            self.show_index()
        elif path == '/currencies':
            self.show_currencies()
        elif path == '/users':
            self.show_users()
        elif path == '/api/currencies':
            self.api_currencies()
        elif path == '/api/subscriptions':
            self.api_subscriptions()
        elif path.startswith('/static/'):
            self.serve_static()
        else:
            self.send_error(404, f"Страница не найдена: {path}")
    
    def do_POST(self):
        """Обработка POST запросов."""
        path = urlparse(self.path).path
        
        if path == '/api/subscribe':
            self.handle_subscribe()
        elif path == '/api/update_currencies':
            self.handle_update_currencies()
        else:
            self.send_error(404, f"API эндпоинт не найден: {path}")
    
    def show_index(self):
        """Главная страница."""
        # Инициализируем компоненты при загрузке
        self._initialize_components()
        currencies = self.currency_service.get_all_currencies()[:3]
        
        template = self.template_env.get_template('index.html')
        html = template.render(
            app=self.app_info,
            currencies=currencies,
            total_currencies=len(self.currency_service.get_all_currencies()),
            total_users=len(self.users)
        )
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def show_currencies(self):
        """Страница валют."""
        self._initialize_components()
        currencies = self.currency_service.get_all_currencies()
        
        template = self.template_env.get_template('currencies.html')
        html = template.render(
            app=self.app_info,
            currencies=currencies
        )
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def show_users(self):
        """Страница пользователей."""
        self._initialize_components()
        
        # Добавляем информацию о подписках
        users_with_subs = []
        for user in self.users:
            subscriptions = []
            for uc in self.user_currencies:
                if uc.user_id == user.id:
                    currency = self.currency_service.get_currency_by_id(uc.currency_id)
                    if currency:
                        subscriptions.append(currency.char_code)
            
            user_dict = {
                'id': user.id,
                'name': user.name,
                'subscriptions': subscriptions
            }
            users_with_subs.append(user_dict)
        
        template = self.template_env.get_template('users.html')
        html = template.render(
            app=self.app_info,
            users=users_with_subs
        )
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def api_currencies(self):
        """API для получения списка валют."""
        self._initialize_components()
        currencies_data = self.currency_service.get_currencies_as_dict()
        self._send_json_response(currencies_data)
    
    def api_subscriptions(self):
        """API для получения подписок пользователя."""
        self._initialize_components()
        query = urlparse(self.path).query
        params = parse_qs(query)
        user_id = int(params.get('user_id', [1])[0])
        
        subscriptions = []
        for uc in self.user_currencies:
            if uc.user_id == user_id:
                currency = self.currency_service.get_currency_by_id(uc.currency_id)
                if currency:
                    subscriptions.append(currency.char_code)
        
        data = {
            'user_id': user_id,
            'subscriptions': subscriptions,
            'count': len(subscriptions)
        }
        
        self._send_json_response(data)
    
    def handle_subscribe(self):
        """Обрабатывает запрос на подписку."""
        self._initialize_components()
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_id = data.get('user_id')
            currency_id = data.get('currency_id')
            
            # Проверка существования пользователя
            user_exists = any(u.id == user_id for u in self.users)
            
            # Проверка существования валюты
            currency_exists = self.currency_service.get_currency_by_id(currency_id)
            
            if user_exists and currency_exists:
                # Проверяем, нет ли уже такой подписки
                existing = any(
                    uc.user_id == user_id and uc.currency_id == currency_id
                    for uc in self.user_currencies
                )
                
                if not existing:
                    # Создаем новую подписку
                    new_id = max([uc.id for uc in self.user_currencies]) + 1 if self.user_currencies else 1
                    new_sub = UserCurrency(new_id, user_id, currency_id)
                    self.user_currencies.append(new_sub)
                    
                    response = {
                        'success': True,
                        'message': 'Подписка успешно добавлена',
                        'subscription_id': new_id
                    }
                    self._send_json_response(response)
                else:
                    response = {
                        'success': False,
                        'message': 'Подписка уже существует'
                    }
                    self._send_json_response(response, 400)
            else:
                response = {
                    'success': False,
                    'message': 'Неверный user_id или currency_id'
                }
                self._send_json_response(response, 400)
                
        except Exception as e:
            response = {
                'success': False,
                'error': str(e)
            }
            self._send_json_response(response, 500)
    
    def handle_update_currencies(self):
        """Обрабатывает запрос на обновление курсов валют."""
        self._initialize_components()
        try:
            # Обновляем курсы через сервис
            updated = self.currency_service.update_currency_values()
            
            if updated:
                response = {
                    'success': True,
                    'message': 'Курсы валют успешно обновлены',
                    'currencies': self.currency_service.get_currencies_as_dict()
                }
                self._send_json_response(response)
            else:
                response = {
                    'success': False,
                    'error': 'Не удалось обновить курсы валют'
                }
                self._send_json_response(response, 500)
                
        except Exception as e:
            response = {
                'success': False,
                'error': f'Внутренняя ошибка сервера: {str(e)}'
            }
            self._send_json_response(response, 500)
    
    def serve_static(self):
        """Отдает статические файлы."""
        path = self.path[1:]  # Убираем первый слеш
        if os.path.exists(path):
            self.send_response(200)
            if path.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            elif path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            elif path.endswith('.png'):
                self.send_header('Content-Type', 'image/png')
            else:
                self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, f"Файл не найден: {path}")
    
    def _initialize_components(self):
        """Инициализирует компоненты приложения."""
        if not hasattr(self, 'app_info'):
            # Инициализация компонентов MVC
            self.author = Author("Платунов Иван", "R3142")
            self.app_info = App("Currency Tracker", "1.0.0", self.author)
            
            # Пользователи
            self.users = [
                User(1, "Алексей Петров"),
                User(2, "Мария Сидорова"),
                User(3, "Дмитрий Иванов")
            ]
            
            # Сервисы
            self.currency_service = CurrencyService()
            
            # Подписки
            self.user_currencies = [
                UserCurrency(1, 1, 1),  # Алексей -> USD
                UserCurrency(2, 1, 2),  # Алексей -> EUR
                UserCurrency(3, 2, 1),  # Мария -> USD
            ]
            
            # Шаблонизатор
            self.template_env = Environment(
                loader=FileSystemLoader('views'),
                autoescape=True
            )
    
    def _send_json_response(self, data, status_code=200):
        """Отправляет JSON ответ."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Отключаем вывод логов в консоль."""
        pass


def create_server(host='localhost', port=8080):
    """Создает и запускает HTTP-сервер."""
    server = HTTPServer((host, port), ApplicationHandler)
    server.serve_forever()