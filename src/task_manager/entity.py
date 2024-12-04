from datetime import date
from enum import Enum

from src.base.entity import BaseEntity


class StatusEnum(Enum):
    """Статусы задачи"""

    NOT_COMPLETED = "Не выполнена"
    COMPLETED = "Выполнена"


class PriorityEnum(Enum):
    """Приоритеты задачи"""

    LOW = "Низкий"
    MEDIUM = "Средний"
    HIGH = "Высокий"


class CategoryEnum(Enum):
    """Категории задачи"""

    WORK = "Работа"
    PRIVATE = "Личное"
    EDUCATION = "Обучение"


class Task(BaseEntity):
    """Класс задачи"""

    id: int
    title: str
    description: str
    category: CategoryEnum
    due_date: date
    priority: PriorityEnum
    status: StatusEnum

    def __str__(self):
        return (f"\nid: {self.id} | {self.title}, {self.description},\n"
                f"Категория {self.category}, выполнить к: {self.due_date}\n"
                f"Приоритет: {self.priority}, статус: {self.status}")

    def check_due_date(self, value: date) -> None:
        """Проверяет, дата завершения задачи наступает или нет"""
        if value < date.today():
            raise ValueError("Дата выполнения задачи должна быть позже текущей или быть текущей")
