from src.base.app import BaseApp


class BaseInteractor:
    def __call__(self):
        """Запускает основную логику"""
        self.start()
        try:
            self.interact()
        finally:
            self.end()

    def interact(self):
        """Взаимодействует с пользователем"""
        raise NotImplementedError

    def start(self):
        """Запускает все приложения"""
        for value in self.__class__.__dict__.values():
            if isinstance(value, BaseApp):
                value.start()

    def end(self):
        """Завершает работу всех приложений"""
        for value in self.__class__.__dict__.values():
            if isinstance(value, BaseApp):
                value.end()
