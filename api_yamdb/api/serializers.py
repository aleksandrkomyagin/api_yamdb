from django.contrib.auth import get_user_model

from rest_framework import serializers


User = get_user_model()


class CreateUserConfirmationCode(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)


class CreateUserToken(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)
