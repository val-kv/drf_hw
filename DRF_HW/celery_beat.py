from celery import Celery
from celery.schedules import crontab
from celery.signals import beat_init
from DRF_HW.celery import app as celery_app

from materials.tasks import check_inactive_users

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')


@beat_init.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0), check_inactive_users)
    celery_app.conf.beat_schedule.update({
        'check_inactive_users_task': {
            'task': 'DRF_HW.tasks.check_inactive_users',
            'schedule': crontab(hour=0, minute=0),
        },
    })


setup_periodic_tasks(celery_app)
