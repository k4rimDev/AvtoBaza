from django.apps import AppConfig


class BaseUserConfig(AppConfig):
    name = 'apps.base_user'
    verbose_name = 'İstifadəçilərə aid olan hissələr'
    
    def ready(self) -> None:
        import apps.account.signals
