from django.apps import AppConfig
import asyncio, threading


class PortDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'port_data'


    def ready(self):
        import port_data.celery_signals