from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.order'
    verbose_name = "Sifarişə aid olan hissələr"
    def ready(self) -> None:
        import apps.order.signals
