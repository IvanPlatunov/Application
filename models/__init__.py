"""Пакет моделей приложения для работы с данными.

Содержит классы предметной области:
- Author: автор проекта
- App: информация о приложении
- User: пользователь системы
- Currency: валюта и ее курс
- UserCurrency: связь пользователей с валютами
"""

from .author import Author
from .app import App
from .user import User
from .currency import Currency
from .user_currency import UserCurrency

__all__ = ['Author', 'App', 'User', 'Currency', 'UserCurrency']