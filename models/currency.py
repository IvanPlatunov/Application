from typing import Union

"""Модель валюты.

Класс Currency представляет валюту с ее атрибутами:
цифровой код, символьный код, название, курс и номинал.
"""


class Currency:
    """Класс для представления валюты и ее курса.

    Attributes:
        id (int): Уникальный идентификатор валюты
        num_code (str): Цифровой код валюты (3 символа)
        char_code (str): Символьный код валюты (3 символа)
        name (str): Название валюты
        value (float): Курс валюты к рублю
        nominal (int): Номинал валюты
    """

    def __init__(
        self,
        id: int,
        num_code: str,
        char_code: str,
        value: float,
        nominal: int,
    ):
        """Инициализирует объект Currency.

        Args:
            id (int): Уникальный идентификатор валюты
            num_code (str): Цифровой код валюты (3 символа)
            char_code (str): Символьный код валюты (3 символа)
            value (float): Курс валюты к рублю
            nominal (int): Номинал валюты

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """
        self.__id: int = id
        self.__num_code: str = num_code
        self.__char_code: str = char_code
        self.__value: float = float(value)
        self.__nominal: int = nominal

        # Валидация
        self._validate_parameters("id", self.__id)
        self._validate_parameters("num_code", self.__num_code)
        self._validate_parameters("char_code", self.__char_code)
        self._validate_parameters("value", self.__value)
        self._validate_parameters("nominal", self.__nominal)

    def _validate_parameters(
        self, type: str, par: int | str | float
    ) -> Union[None, bool]:
        """Выполняет валидацию всех параметров валюты."""
        if type == "id":
            if not isinstance(par, int) or par <= 0:
                raise ValueError("ID валюты должен быть положительным целым числом")
            return True

        elif type == "num_code":
            if not isinstance(par, str) or len(par) != 3:
                raise ValueError("Цифровой код валюты должен состоять из 3 символов")
            return True

        elif type == "char_code":
            if not isinstance(par, str) or len(par) != 3:
                raise ValueError("Символьный код валюты должен состоять из 3 символов")
            return True

        elif type == "value":
            if not isinstance(par, (int, float)) or par <= 0:
                raise ValueError("Курс валюты должен быть положительным числом")
            return True

        elif type == "nominal":
            if not isinstance(par, int) or par <= 0:
                raise ValueError(
                    "Номинал валюты должен быть положительным целым числом"
                )
            return True

    @property
    def id(self) -> int:
        """Возвращает уникальный идентификатор валюты.

        Returns:
            int: ID валюты
        """
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        """Устанавливает ID валюты с валидацией.

        Args:
            id (int): Новый ID валюты

        Raises:
            ValueError: Если ID не соответствует требованиям
        """
        if self._validate_parameters('id', id):
            self.__id = id

    @property
    def num_code(self) -> str:
        """Возвращает цифровой код валюты.

        Returns:
            str: Цифровой код (3 символа)
        """
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: str) -> None:
        """Устанавливает цифровой код валюты с валидацией.

        Args:
            num_code (str): Новый цифровой код

        Raises:
            ValueError: Если код не соответствует требованиям
        """
        if self._validate_parameters('num_code', num_code):
            self.__num_code = num_code

    @property
    def char_code(self) -> str:
        """Возвращает символьный код валюты.

        Returns:
            str: Символьный код (3 символа)
        """
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str) -> None:
        """Устанавливает символьный код валюты с валидацией.

        Args:
            char_code (str): Новый символьный код

        Raises:
            ValueError: Если код не соответствует требованиям
        """
        if self._validate_parameters('char_code', char_code):
            self.__char_code = char_code


    @property
    def value(self) -> float:
        """Возвращает курс валюты.

        Returns:
            float: Курс валюты к рублю
        """
        return self.__value

    @value.setter
    def value(self, value: float) -> None:
        """Устанавливает курс валюты с валидацией.

        Args:
            value (float): Новый курс валюты

        Raises:
            ValueError: Если курс не соответствует требованиям
        """
        if self._validate_parameters('value', value):
            self.__value = value

    @property
    def nominal(self) -> int:
        """Возвращает номинал валюты.

        Returns:
            int: Номинал валюты
        """
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int) -> None:
        """Устанавливает номинал валюты с валидацией.

        Args:
            nominal (int): Новый номинал валюты

        Raises:
            ValueError: Если номинал не соответствует требованиям
        """
        if self._validate_parameters('nominal', nominal):
            self.__nominal = nominal

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта Currency
        """
        return f"Currency(id={self.__id}, char_code='{self.__char_code}', value={self.__value})"
