"""Модель приложения.

Класс App представляет информацию о приложении,
включая название, версию и автора.
"""

from .author import Author
from typing import Union


class App:
    """Класс для представления информации о приложении.

    Attributes:
        name (str): Название приложения
        version (str): Версия приложения
        author (Author): Автор приложения
    """

    def __init__(self, name: str, version: str, author: Author):
        """Инициализирует объект App.

        Args:
            name (str): Название приложения
            version (str): Версия приложения
            author (Author): Объект Author - автор приложения

        """
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

        # Валидация
        self._validate_parameters("name", self.__name)
        self._validate_parameters("version", self.__version)
        self._validate_parameters("author", self.__author)

    def _validate_parameters(self, type: str, par: str | Author) -> Union[bool, None]:
        """Проверяет корректность вводимых данных

        Args:
            type (str): тип вводимых данных
            par (Author|str): параметр для проверки корректности

        Returnes:
            True если введенный параметр соответсвует заданным требованиям, None если нет

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """

        if type == "name":
            if not isinstance(par, str) or len(par) < 1:
                raise ValueError("Название приложения должно быть непустой строкой")
            return True
        elif type == "version":
            if not isinstance(par, str) or len(par) < 1:
                raise ValueError("Версия приложения должна быть непустой строкой")
            return True
        elif type == "author":
            if not isinstance(par, Author):
                raise ValueError("Автор должен быть объектом класса Author")
            return True

    @property
    def name(self) -> str:
        """Возвращает название приложения.

        Returns:
            str: Название приложения
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Устанавливает название приложения с валидацией.

        Args:
            name (str): Новое название приложения

        Raises:
            ValueError: Если название не соответствует требованиям
        """
        if self._validate_parameters("name", name):
            self.__name = name

    @property
    def version(self) -> str:
        """Возвращает версию приложения.

        Returns:
            str: Версия приложения
        """
        return self.__version

    @version.setter
    def version(self, version: str) -> None:
        """Устанавливает версию приложения с валидацией.

        Args:
            version (str): Новая версия приложения

        Raises:
            ValueError: Если версия не соответствует требованиям
        """
        if self._validate_parameters("version", version):
            self.__version = version

    @property
    def author(self) -> Author:
        """Возвращает автора приложения.

        Returns:
            Author: Объект Author - автор приложения
        """
        return self.__author

    @author.setter
    def author(self, author: Author) -> None:
        """Устанавливает автора приложения с валидацией.

        Args:
            author (Author): Новый автор приложения

        Raises:
            ValueError: Если автор не является объектом класса Author
        """
        if self._validate_parameters("author", author):
            self.__author = author

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта App
        """
        return f"App(name='{self.__name}', version='{self.__version}', author={self.__author})"
