from django.apps import AppConfig


class FillInDocxConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fill_in_docx"

    def ready(self):
        import fill_in_docx.signals  # Підключення сигналів
