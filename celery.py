import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Portfolio_Erick.settings')

app = Celery('Portfolio_Erick')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
