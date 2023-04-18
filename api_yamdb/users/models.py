from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username

USER = 'user'
STAFF = 'staff'
ADMIN = 'admin'
MODERATOR = 'moderator'
SUPERUSER = 'superuser'

ROLE_CHOICES = [
    (STAFF, STAFF),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (SUPERUSER, SUPERUSER),
]


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.role == STAFF
            or self.role == SUPERUSER
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField('код подтверждения', unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='code',
        verbose_name='пользователь',
    )
    created = models.DateTimeField('дата верификации', auto_now_add=True)

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'
