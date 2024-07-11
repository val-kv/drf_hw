from celery.task import periodic_task
from celery.schedules import crontab

@periodic_task(run_every=(crontab(minute='*/15')))
def my_periodic_task():
    # Ваш код периодической задачи
    pass