from typing import Union
"""Модель пользователя.

Класс User представляет пользователя системы
с уникальным идентификатором и именем.
"""


class User:
    """Класс для представления пользователя системы.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Имя пользователя
    """

    def __init__(self, id: int, name: str):
        """Инициализирует объект User.

        Args:
            id (int): Уникальный идентификатор пользователя
            name (str): Имя пользователя

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """
        self.__id: int = id
        self.__name: str = name

        # Валидация
        self._validate_parameters('id', self.__id)
        self._validate_parameters('name', self.__name)



    def _validate_parameters(self, type: str, par: str|int ) -> Union[bool, None]:
        """Проверяет корректность вводимых данных

        Args:
            type (str): тип вводимых данных
            par (Author|str): параметр для проверки корректности

        Returnes:
            True если введенный параметр соответсвует заданным требованиям, None если нет

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """

        if type == "id":
            if not isinstance(par, int) or par <= 0:
                raise ValueError("ID пользователя должен быть положительным целым числом")
            return True
        elif type == "name":
            if not isinstance(par, str) or len(par) < 2:
                raise ValueError("Имя пользователя должно быть строкой длиной не менее 2 символов")
            return True

    @property
    def id(self) -> int:
        """Возвращает уникальный идентификатор пользователя.

        Returns:
            int: ID пользователя
        """
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        """Устанавливает ID пользователя с валидацией.

        Args:
            id (int): Новый ID пользователя

        Raises:
            ValueError: Если ID не соответствует требованиям
        """
        if self._validate_parameters('id', id):
            self.__id = id

    @property
    def name(self) -> str:
        """Возвращает имя пользователя.

        Returns:
            str: Имя пользователя
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Устанавливает имя пользователя с валидацией.

        Args:
            name (str): Новое имя пользователя

        Raises:
            ValueError: Если имя не соответствует требованиям
        """
        if self._validate_parameters('name', name):
            self.__name= name


    def __repr__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта User
        """
        return f"User(id={self.__id}, name='{self.__name}')"
