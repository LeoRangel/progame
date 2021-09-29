from django.apps import AppConfig


class AusersConfig(AppConfig):
    name = 'ausers'
    verbose_name = 'aUsers'

    def ready(self):
        import ausers.signals.handlers
