from django.apps import AppConfig


class ProgameConfig(AppConfig):
    name = 'progame'
    verbose_name = 'ProGame'

    def ready(self):
        import progame.signals.handlers
        import progame.signals.conquistas
