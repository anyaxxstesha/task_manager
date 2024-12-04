class BaseApp:
    """Базовый класс приложения"""

    def start(self):
        """Запускает приложение"""
        raise NotImplementedError

    def end(self):
        """Останавливает работу приложения"""
        raise NotImplementedError
