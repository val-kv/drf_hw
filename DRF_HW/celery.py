import eventlet
import os
from celery import Celery

eventlet.monkey_patch()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_HW.settings')

app = Celery('DRF_HW')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
