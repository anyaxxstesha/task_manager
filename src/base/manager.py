from typing import Self, Any, Type

from src.base.loader import BaseFileLoader
from src.task_manager.entity import BaseEntity
from src.base.repr_mixin import ReprMixin


class BaseManager(ReprMixin):
    """Базовый класс менеджера для работы с сущностями"""
    loader: BaseFileLoader = None
    model: Type[BaseEntity] = None
    _id: int = 1

    def __init__(self, entities: list | None = None):
        self._entities = entities or []


    def search(self, **kwargs) -> list:
        """
        Производит поиск по точному соответствию
        переданных аргументов
        """
        sorted_entities = self._entities
        for param, value in kwargs.items():
            sorted_entities = filter(
                lambda x: getattr(x, param, None) == value,
                sorted_entities
            )
        return list(sorted_entities)

    def search_by_keyword(self, keyword: str) -> list[BaseEntity]:
        """
        Производит поиск по ключевому слову
        """
        sorted_entities = []
        for entity in self._entities:
            to_search = entity.get_text_fields()
            for value in to_search.values():
                if keyword in value:
                    sorted_entities.append(entity)
                    break
        return sorted_entities

    def search_with_index(self, **kwargs) -> list[tuple]:
        """
        Производит поиск по точному соответствию
        переданных аргументов.
        Возвращает первую соответствующую сущность
        и ее индекс
        """
        sorted_entities = []
        for index, entity in zip(range(len(self._entities)), self._entities):
            if all(getattr(entity, param, None) == value for param, value in kwargs.items()):
                sorted_entities.append((entity, index))
        return sorted_entities

    @property
    def next_id(self) -> int:
        _next = self._id
        self._id += 1
        return _next

    def serialize(self) -> list[dict[str, Any]]:
        """Преобразует все сущности в словари"""
        return [entity.serialize() for entity in self._entities]

    @classmethod
    def deserialize(cls, entities: list[dict[str, Any]]) -> list[BaseEntity]:
        """Преобразует данные в список объектов Entity"""
        return [cls.model(**entity_dict) for entity_dict in entities]

    def dump(self) -> None:
        """Сериализует все сущности"""
        if not self.loader:
            raise NotImplementedError("Не установлен загрузчик")
        serialized_entities = self.serialize()
        to_dump = {
            "meta": {"next_id": self._id},
            "data": serialized_entities
        }
        self.loader.dump(to_dump)

    @classmethod
    def load(cls) -> Self:
        """Десериализует все сущности"""
        if not cls.loader:
            raise NotImplementedError("Не установлен загрузчик")
        try:
            loaded = cls.loader.load()
        except FileNotFoundError:
            return cls()
        data = loaded.get("data", [])
        cls._id = loaded.get("meta", {}).get("next_id", len(data) + 1)
        entities = cls.deserialize(data)
        return cls(entities)
