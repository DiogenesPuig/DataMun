from django.apps import AppConfig


class DatamunConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dataMun'
    def ready(self):
        import dataMun.signals