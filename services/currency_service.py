"""Сервис для работы с валютами."""

from typing import List, Dict, Any, Optional
from models.currency import Currency
from utils.currencies_api import get_currencies


class CurrencyService:
    """Сервис для управления валютами."""
    
    def __init__(self):
        self._currencies: List[Currency] = []
        self._currency_codes = ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'CHF', 'CAD']
        self._load_currencies()
    
    def _load_currencies(self):
        """Загружает валюты из внешнего API или создает демо-данные."""
        try:
            raw_currencies = get_currencies(self._currency_codes)
            
            for i, (code, value) in enumerate(raw_currencies.items(), 1):
                currency = Currency(
                    id=i,
                    num_code=str(100 + i),
                    char_code=code,
                    value=value,
                    nominal=1
                )
                self._currencies.append(currency)
        except Exception as e:
            print(f"Ошибка загрузки валют: {e}")
    
    def get_all_currencies(self) -> List[Currency]:
        return self._currencies
    
    def get_currency_by_id(self, currency_id: int) -> Optional[Currency]:
        for currency in self._currencies:
            if currency.id == currency_id:
                return currency
        return None
    
    def get_currency_by_code(self, char_code: str) -> Optional[Currency]:
        for currency in self._currencies:
            if currency.char_code == char_code:
                return currency
        return None
    
    def update_currency_values(self) -> bool:
        """Обновляет курсы валют из внешнего API."""
        try:
            raw_currencies = get_currencies(self._currency_codes)
            
            updated = False
            for currency in self._currencies:
                if currency.char_code in raw_currencies:
                    new_value = raw_currencies[currency.char_code]
                    if new_value != currency.value:
                        currency.value = new_value
                        updated = True
            
            if not updated and raw_currencies:
                # Если валюты не обновились, но данные получены, перезагружаем
                self._currencies.clear()
                self._load_currencies()
                updated = True
            
            return updated
        except Exception as e:
            print(f"Ошибка обновления курсов: {e}")
            return False
    
    def get_currencies_as_dict(self) -> List[Dict[str, Any]]:
        result = []
        for currency in self._currencies:
            result.append({
                'id': currency.id,
                'num_code': currency.num_code,
                'char_code': currency.char_code,
                'value': currency.value,
                'nominal': currency.nominal
            })
        return result