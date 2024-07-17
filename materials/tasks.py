from django.utils import timezone
from django.contrib.auth.models import User
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()

        subject = f'Аккаунт пользователя {user.username} был удален'
        message = f'Аккаунт пользователя {user.username} был удален.'
        from_email = 'your_email@example.com'
        recipient_list = [user.email]
        send_email_task.delay(subject, message, from_email, recipient_list)

        print(f'Аккаунт пользователя {user.username} был удален')
