from celery import Celery
from celery.schedules import crontab
from django.utils import timezone
from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail


app = Celery('tasks', broker='redis://localhost:6379/0')


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@app.task
def check_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()


app.conf.beat_schedule = {
    'check_inactive_users_task': {
        'task': 'tasks.check_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}