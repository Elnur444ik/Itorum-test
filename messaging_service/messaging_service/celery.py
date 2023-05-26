import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_service')

app = Celery('send_message')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()