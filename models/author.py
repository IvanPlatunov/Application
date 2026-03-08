from typing import Any

"""Модель автора проекта.

Класс Author представляет автора приложения с атрибутами
имени и учебной группы.
"""


class Author:
    """Класс для представления автора проекта.

    Attributes:
        name (str): Имя автора
        group (str): Учебная группа автора
    """

    def __init__(self, name: str, group: str):
        """Инициализирует объект Author.

        Args:
            name (str): Имя автора, должно содержать не менее 2 символов
            group (str): Учебная группа автора, непустая строка

        Raises:
            ValueError: Если параметры не соответствуют требованиям
        """
        self.__name: str = name
        self.__group: str = group

        # Валидация при инициализации
        self._validate_parameters("name", self.name)
        self._validate_parameters("group", self.group)

    def _validate_parameters(self, type: str, par: str) -> Any:
        if type == "name":
            if not isinstance(par, str) or len(par) < 2:
                raise ValueError(
                    "Имя автора должно быть строкой длиной не менее 2 символов"
                )
            return True
        elif type == "group":
            if not isinstance(par, str) or len(par) == 0:
                raise ValueError("Учебная группа автора должна быть непустой строкой")
            return True

    @property
    def name(self) -> str:
        """Возвращает имя автора.

        Returns:
            str: Имя автора
        """
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Устанавливает имя автора с валидацией.

        Args:
            name (str): Новое имя автора

        Raises:
            ValueError: Если имя не соответствует требованиям
        """
        if self._validate_parameters("name", name):
            self.__name = name

    @property
    def group(self) -> str:
        """Возвращает учебную группу автора.

        Returns:
            str: Учебная группа
        """
        return self.__group

    @group.setter
    def group(self, group: str) -> None:
        """Устанавливает учебную группу автора с валидацией.

        Args:
            group (str): Новая учебная группа

        Raises:
            ValueError: Если группа не соответствует требованиям
        """
        if self._validate_parameters("group", group):
            self.__group = group

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта.

        Returns:
            str: Строковое представление объекта Author
        """
        return f"Author(name='{self.__name}', group='{self.__group}')"
