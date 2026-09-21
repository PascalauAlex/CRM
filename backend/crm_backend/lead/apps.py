from django.apps import AppConfig


class LeadConfig(AppConfig):
    name = 'lead'

    def ready(self) -> None:
        from . import signals
