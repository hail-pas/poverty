from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = '后台管理'

    def ready(self):
        import api.signals
