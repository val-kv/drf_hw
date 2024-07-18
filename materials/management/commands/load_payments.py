from django.core.management.base import BaseCommand
from users.models import Payments
from datetime import datetime


class Command(BaseCommand):
    help = 'Загрузите примерные данные о платежах в таблицу платежей'

    def handle(self, *args, **kwargs):
        # Создаем данные платежей
        Payments.objects.create(user_id=1, payment_date=datetime.now(), paid_course_id=1, amount=50.00, payment_method='cash')
        Payments.objects.create(user_id=2, payment_date=datetime.now(), paid_course_id=2, paid_lesson_id=1, amount=25.00, payment_method='transfer')

        self.stdout.write(self.style.SUCCESS('Данные о платежах загружены'))
