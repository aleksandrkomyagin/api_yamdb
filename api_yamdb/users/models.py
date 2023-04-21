import uuid

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models

from users.validators import validate_username

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR)
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

    confirmation_code = models.UUIDField(
        'код подтверждения',
        unique=True,
        max_length=255,
        null=True,
        blank=False)

    def save(self, *args, **kwargs):
        self.confirmation_code = uuid.uuid4()
        super(User, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return bool(
            self.is_superuser
            or self.role == ADMIN
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def send_mail(self):
        send_mail(
            subject='Confirmation Code',
            message=f'Ваш код активации: {self.confirmation_code}',
            recipient_list=[self.email, ],
            from_email='from@example.com',
        )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
