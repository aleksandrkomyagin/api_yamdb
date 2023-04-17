import datetime as dt

from rest_framework import serializers


def validate_year(value):
    if dt.date.today().year < value:
        raise serializers.ValidationError(
            'Год создания не может быть больше текущего'
        )
    return value
