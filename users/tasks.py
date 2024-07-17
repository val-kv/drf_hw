from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.utils import timezone
from celery import shared_task

logger = get_task_logger(__name__)


@shared_task
def check_inactive_users():
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timezone.timedelta(days=30), is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f"User {user.username} has been blocked due to inactivity.")