from __future__ import absolute_import, unicode_literals

import eventlet
import os
from celery import Celery

eventlet.monkey_patch()

# Set the timezone for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRF_HW.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Kaliningrad'  # Часовой пояс для Celery