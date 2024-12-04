from src.base.interact_utils import cast_int
from src.base.interactor import BaseInteractor
from src.config import settings
from src.task_manager import TaskManagerApp, task_manager_app


class Interactor(BaseInteractor):
    """Класс для работы с пользователем"""

    task_manager_app: TaskManagerApp = task_manager_app

    def interact(self):
        while True:
            print("\nВыберите действие:")
            print("1. Создать задачу")
            print("2. Найти задачу/задачи по ключевому слову, статусу или категории")
            print("3. Просмотреть список всех задач")
            print("4. Редактировать задачу")
            print("5. Изменить статус задачи")
            print("6. Удалить задачу")
            print("0. Выйти")
            try:
                choice = cast_int(input("Ваш выбор: "))

                if choice == 1:
                    self.task_manager_app.create()
                elif choice == 2:
                    self.task_manager_app.sorted_list()
                elif choice == 3:
                    self.task_manager_app.list()
                elif choice == 4:
                    self.task_manager_app.update()
                elif choice == 5:
                    self.task_manager_app.update_status()
                elif choice == 6:
                    self.task_manager_app.delete()
                elif choice == 0:
                    break
                else:
                    print("Неверный ввод. Попробуйте снова.")
            except (ValueError, TypeError) as exc:
                if settings.DEBUG:
                    raise
                else:
                    print(f"Ошибка: {exc.args[0]}")
