from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    
    def ready(self):
        # Импортируем здесь, чтобы избежать циклических импортов
        from .model_loader import load_models
        load_models()
