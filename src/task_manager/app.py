from datetime import date

from src.base.app import BaseApp
from src.base.interact_utils import cast_int, pretty_list
from src.task_manager.manager import TaskManager
from src.base.repr_mixin import ReprMixin


class TaskManagerApp(ReprMixin, BaseApp):
    """Основной класс, реализующий взаимодействие с пользователем."""
    manager: TaskManager

    def start(self):
        """Запускает приложение"""
        self.manager = TaskManager.load()

    def end(self):
        """Останавливает приложение"""
        self.manager.dump()


    def create(self):
        """Создает экземпляр задачи и выводит пользователю сообщение об успешном создании"""
        print("Введите данные для создания задачи:")
        title = input("Название: ")
        description = input("Описание: ")
        category = input("Категория задачи, e.g. 'Работа', 'Личное' или 'Обучение': ")
        due_date = input("Дата завершения задачи, в формате yyyy-mm-dd, 2024-12-5: ")
        priority = input("Приоритет задачи, e.g. 'Низкий', 'Средний' или 'Высокий': ")
        result = self.manager.create(title=title, description=description, category=category, due_date=due_date,
                                     priority=priority)

        print(f"Создана задача: {result}")

    def sorted_list(self):
        """Выводит пользователю список всех задач, соответствующих определенным параметрам"""
        print("Введите: для поиска по ключевому слову - 1,\n"
              "для поиска по статусу и категории - другое значение")
        search_by_keywoprd = input("Ваш выбор: ")
        if search_by_keywoprd == "1":
            key_word = input("Ключевое слово: ")
            result = self.manager.search_by_keyword(key_word)
        else:
            print("Ненужный параметр пропустить, нажав Enter")
            status = input("Статус, e.g. 'Не выполнена' или 'Выполнена': ")
            category = input("Категория задачи, e.g. 'Работа', 'Личное' или 'Обучение': ")
            search_params = {}
            if status:
                search_params['status'] = status
            if category:
                search_params['category'] = category
            result = self.manager.search(**search_params)

        print(f"Найдены задачи:")
        pretty_list(result)

    def list(self):
        """Выводит пользователю список всех задач"""

        result = self.manager.search()

        print(f"Все имеющиеся задачи:")
        pretty_list(result)

    def update(self):
        """Редактирование задачи"""
        print("Введите данные для изменения задачи:")
        task_id = cast_int(input("id задачи: "))
        to_update = {
            "title": input("Название: "),
            "description": input("Описание: "),
            "category": input("Категория (Работа, личное, обучение): "),
            "due_date": input("Дата завершения задачи, в формате yyyy-mm-dd, 2024-12-5: "),
            "priority": input("Приоритет задачи, e.g. 'Низкий', 'Средний' или 'Высокий': ")
        }

        result = self.manager.update(task_id, **to_update)

        print(f"Задача после изменения статуса: {result}")


    def update_status(self):
        """Выводит пользователю задачу после изменения ее статуса"""
        print("Введите данные для изменения статуса задачи:")
        task_id = cast_int(input("id задачи: "))
        status = input("Статус, e.g. 'Не выполнена' или 'Выполнена': ")

        result = self.manager.update(task_id, status=status)

        print(f"Задача после изменения статуса: {result}")

    def delete(self):
        """Выводит пользователю удаленную задачу"""
        print("Введите данные для удаления задачи: ")
        task_id = cast_int(input("id задачи: "))

        result = self.manager.delete(task_id)

        print(f"Удалена задача: {result}")

