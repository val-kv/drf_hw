from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the timezone for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_HW.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Australia/Tasmania'  # Set the timezone here