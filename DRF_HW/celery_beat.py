from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init
from DRF_HW.celery import app as celery_app
from celery.task import periodic_task

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

@beat_init.connect
def setup_periodic_tasks(sender, **kwargs):
    # Определите ваши периодические задачи здесь
    # Пример:
    celery_app.conf.beat_schedule.update({
        'my_task': {
            'task': 'DRF_HW.tasks.my_task',
            'schedule': crontab(minute='*/5'),
        },
    })

# Определите вашу задачу здесь
@periodic_task(run_every=crontab(minute='*/5'))
def my_task():
    # Ваш код для выполнения задачи
    pass