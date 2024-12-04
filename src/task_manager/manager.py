from typing import Type

from src.base.loader import JSONFileLoader
from src.base.manager import BaseManager
from src.config import settings
from src.task_manager.entity import Task, StatusEnum


class TaskManager(BaseManager):
    """Менеджер для работы с задачами"""

    loader: JSONFileLoader = JSONFileLoader(settings.FILE_PATH)
    model: Type[Task] = Task

    def create(self, **data) -> Task:
        """Создает новую задачу"""
        task = self.model(id=self.next_id, status=StatusEnum.NOT_COMPLETED, **data)
        self._entities.append(task)
        return task

    def read_all(self, **kwargs) -> list[Task]:
        """
        Возвращает список, отфильтрованный по точному соответствию kwargs.
        Если kwargs не были переданы - возвращает все задачи.
        """
        return self.search(**kwargs)

    def update(self, task_id: int, **kwargs) -> Task | None:
        """Изменяет задачу"""
        result = self.search_with_index(id=task_id)
        (task, _), *_ = result or [(None, None)]
        if task is None:
            raise ValueError("Задача для обновления не найдена")
        for k, v in kwargs.items():
            setattr(task, k, v)
        return task

    def delete(self, task_id: int) -> Task:
        """Удаляет задачу"""
        result = self.search_with_index(id=task_id)
        (task, index), *_ = result or [(None, None)]
        if task is None:
            raise ValueError("Задача для удаления не найдена")
        self._entities.pop(index)
        return task

    def delete_many(self, **kwargs) -> list[Task]:
        """Удаляет задачи, соответствующие переданным параметрам"""
        result = self.search_with_index(**kwargs)
        return [self._entities.pop(index) for _, index in result]
