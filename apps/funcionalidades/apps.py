from django.apps import AppConfig


class FuncionalidadesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'funcionalidades'

    def ready(self):
        import funcionalidades.signals
