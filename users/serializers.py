from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = ['email', 'password', 'first_name', 'last_name']