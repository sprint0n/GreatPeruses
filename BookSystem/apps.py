from django.apps import AppConfig


class BooksystemConfig(AppConfig):
    name = 'BookSystem'

    def ready(self):
        import BookSystem.signals