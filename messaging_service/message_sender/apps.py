from django.apps import AppConfig


class MessageSenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_sender'

    def ready(self):
        import message_sender.signals
