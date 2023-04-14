import datetime as dt
import re

from django.core.exceptions import ValidationError
from rest_framework import serializers


def validate_username(value):
    if value == 'me':
        raise serializers.ValidationError(
            'Нельзя использовать юзернэйм <me>.',
            {'value': value}
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise serializers.ValidationError(
            f'Не допустимые символы <{value}> в нике.',
            {'value': value}
        )


def validate_year(value):
    if dt.date.today().year < value:
        raise ValidationError(
            'Год создания не может быть больше текущего'
        )
    return value
