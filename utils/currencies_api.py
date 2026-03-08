"""Модуль для работы с API курсов валют.

Предоставляет функцию для получения актуальных курсов валют
с сайта Центрального Банка Российской Федерации.
"""

import requests
from xml.etree import ElementTree
from typing import Dict, Optional


def get_currencies(currency_codes: Optional[list] = None) -> Dict[str, float]:
    """Получает актуальные курсы валют с сайта ЦБ РФ.
    
    Функция загружает XML-данные с курсами валют, парсит их
    и возвращает словарь с курсами для указанных валют.
    
    Args:
        currency_codes (list, optional): Список символьных кодов валют
            для фильтрации (например, ['USD', 'EUR']).
            Если None, возвращаются все доступные валюты.
    
    Returns:
        Dict[str, float]: Словарь, где ключи - символьные коды валют,
            значения - курсы к рублю для номинала 1.
    
    Raises:
        requests.RequestException: При ошибке сетевого запроса
        ValueError: При ошибке парсинга XML-данных
    
    Example:
        >>> get_currencies(['USD', 'EUR'])
        {'USD': 75.50, 'EUR': 85.30}
    """
    try:
        # URL API Центрального Банка РФ
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        
        # Отправка HTTP GET запроса
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на ошибки HTTP
        
        # Парсинг XML-ответа
        root = ElementTree.fromstring(response.content)
        
        currencies = {}
        
        # Обработка каждой валюты в XML
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            value_str = valute.find('Value').text
            nominal = int(valute.find('Nominal').text)
            
            # Преобразование строки значения в число
            value = float(value_str.replace(',', '.'))
            
            # Если заданы конкретные валюты, фильтруем их
            if currency_codes and char_code not in currency_codes:
                continue
            
            # Приводим курс к номиналу 1
            currencies[char_code] = value / nominal
        
        return currencies
        
    except requests.RequestException as e:
        raise requests.RequestException(f"Ошибка сетевого запроса: {e}")
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Ошибка парсинга данных: {e}")
    except Exception as e:
        raise Exception(f"Непредвиденная ошибка: {e}")