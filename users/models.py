from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.conf import settings
from materials.models import Lesson, Course


class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    phone = models.CharField(max_length=12, null=True, blank=True)
    city = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)


