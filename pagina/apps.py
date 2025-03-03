from django.apps import AppConfig

class PaginaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pagina'

    def ready(self):
        import pagina.signals  # Importa las señales para que se registren
