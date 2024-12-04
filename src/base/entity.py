from datetime import date, datetime
from enum import Enum
from typing import Self, Any

from src.base.repr_mixin import ReprMixin


class BaseEntity(ReprMixin):
    """Базовый класс сущности"""

    def __init__(self, **kwargs) -> None:
        """Инициализатор экземпляра класса"""

        for field_name in self.__annotations__.keys():
            value = kwargs.get(field_name, ...)
            setattr(self, field_name, value)

    def __setattr__(self, key: str, value: Any) -> None:
        """Переопределяет метод __setattr__ для валидации значений полей"""
        self._validate(key, value)
        super().__setattr__(key, value)

    def _validate(self, field_name: str, value: Any = ...) -> Any:
        """Валидация поля по имени и значению"""
        if value is ...:
            raise ValueError(f"Пропущено обязательное поле: {field_name}")

        field_type = self.__class__.__annotations__.get(field_name, ...)
        if not isinstance(value, field_type):
            try:
                if issubclass(field_type, date):
                    value = self._validate_date(value)
                else:
                    value = field_type(value)
                custom_validator = getattr(self, f"check_{field_name}", None)
                if custom_validator:
                    custom_validator(value)
            except TypeError as exc:
                raise TypeError(
                    f"Некорректный тип для поля: {field_name}"
                    f" (ожидалось {field_type.__name__}, получено {value.__class__.__name__}: {value})")  from exc
        return value

    def _validate_date(self, value: str) -> date:
        """Валидация даты"""
        date_format = self.get_date_format()
        try:
            return datetime.strptime(value, date_format).date()
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {value}, ожидаемый формат: {date_format}")

    def serialize(self) -> dict[str, Any]:
        """Преобразует экземпляр класса в словарь"""
        serialized = {}
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, Enum):
                field_value = field_value.value
            if isinstance(field_value, date):
                field_value = field_value.strftime(self.get_date_format())
            serialized[field_name] = field_value
        return serialized

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Self:
        """Создает экземпляр класса из словаря"""
        return cls(**data)

    @staticmethod
    def get_date_format():
        """Возвращает формат даты"""
        return "%Y-%m-%d"

    def get_text_fields(self) -> dict[str: str]:
        """Возвращает словарь с текстовыми полями и их занчениями."""
        return {
            field_name: field_value for field_name, field_value in
            self.serialize().items() if isinstance(field_value, str)
        }
