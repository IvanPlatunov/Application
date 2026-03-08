from typing import Union

"""Модель связи пользователь-валюта.

Класс UserCurrency реализует связь многие-ко-многим
между пользователями и валютами.
"""


class UserCurrency:
    """Класс для представления связи между пользователем и валютой.

    Attributes:
        id (int): Уникальный идентификатор связи
        user_id (int): ID пользователя
        currency_id (int): ID валюты
    """

    def __init__(self, id: int, user_id: int, currency_id: int):
        """Инициализирует объект UserCurrency.

        Args:
            id (int): Уникальный идентификатор связи
            user_id (int): ID пользователя
            currency_id (int): ID валюты

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """
        self.__id: int = id
        self.__user_id: int = user_id
        self.__currency_id: int = currency_id

        # Валидация
        self._validate_parameters("id", self.__id)
        self._validate_parameters("user_id", self.__user_id)
        self._validate_parameters("currency_id", self.__currency_id)

    def _validate_parameters(self, type: str, par: int) -> Union[None, bool]:
        if type == "id":
            if not isinstance(par, int) or par <= 0:
                raise ValueError("ID связи должен быть положительным целым числом")
            return True

        elif type == "user_id":
            if not isinstance(par, int) or par <= 0:
                raise ValueError("User ID должен быть положительным целым числом")
            return True
        elif type == "currency_id":
            if not isinstance(par, int) or par <= 0:
                raise ValueError("Currency ID должен быть положительным целым числом")
            return True

    @property
    def id(self) -> int:
        """Возвращает уникальный идентификатор связи.

        Returns:
            int: ID связи
        """
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        """Устанавливает ID связи с валидацией.

        Args:
            id (int): Новый ID связи

        Raises:
            ValueError: Если ID не соответствует требованиям
        """
        if self._validate_parameters("id", id):
            self.__id = id

    @property
    def user_id(self) -> int:
        """Возвращает ID пользователя.

        Returns:
            int: User ID
        """
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Устанавливает User ID с валидацией.

        Args:
            user_id (int): Новый User ID

        Raises:
            ValueError: Если User ID не соответствует требованиям
        """
        if self._validate_parameters("user_id", user_id):
            self.__user_id = user_id

    @property
    def currency_id(self) -> int:
        """Возвращает ID валюты.

        Returns:
            int: Currency ID
        """
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: int) -> None:
        """Устанавливает Currency ID с валидацией.

        Args:
            currency_id (int): Новый Currency ID

        Raises:
            ValueError: Если Currency ID не соответствует требованиям
        """
        if self._validate_parameters("currency_id", currency_id):
            self.__currency_id = currency_id

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта UserCurrency
        """
        return f"UserCurrency(id={self.__id}, user_id={self.__user_id}, currency_id={self.__currency_id})"
