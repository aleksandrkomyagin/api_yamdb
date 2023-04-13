from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'биография',
        blank=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='code'
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'


class Categories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)


class Genres(models.Model):
    name = models.CharField(max_length=56, unique=True)
    slug = models.SlugField(unique=True)


class Titles(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    year = models.DateField()
    category = models.ForeignKey(Categories,
                                 on_delete=models.SET_NULL,
                                 related_name='titles',
                                 null=True)
    ganre = models.ManyToManyField(Genres, through=TitleGenres)


class TitleGenres (models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
