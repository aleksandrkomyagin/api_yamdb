from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

# from .validators import validate_username, validate_year
from .validators import validate_year

# USER = 'user'
# ADMIN = 'admin'
# MODERATOR = 'moderator'

# ROLE_CHOICES = [
#     (USER, USER),
#     (ADMIN, ADMIN),
#     (MODERATOR, MODERATOR),
# ]


# class User(AbstractUser):
#     username = models.CharField(
#         validators=(validate_username,),
#         max_length=150,
#         unique=True,
#         blank=False,
#         null=False
#     )
#     email = models.EmailField(
#         max_length=254,
#         unique=True,
#         blank=False,
#         null=False
#     )
#     role = models.CharField(
#         'роль',
#         max_length=20,
#         choices=ROLE_CHOICES,
#         default=USER,
#         blank=True
#     )
#     bio = models.TextField(
#         'биография',
#         blank=True,
#     )
#     first_name = models.CharField(
#         'имя',
#         max_length=150,
#         blank=True
#     )
#     last_name = models.CharField(
#         'фамилия',
#         max_length=150,
#         blank=True
#     )

#     @property
#     def is_user(self):
#         return self.role == USER

#     @property
#     def is_admin(self):
#         return self.role == ADMIN

#     @property
#     def is_moderator(self):
#         return self.role == MODERATOR

#     class Meta:
#         ordering = ('id',)
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'

#     def __str__(self):
#         return self.username


# class EmailVerification(models.Model):
#     code = models.UUIDField(unique=True)
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='code'
#     )
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'EmailVerification object for {self.user.email}'
User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year],
        db_index=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр',
        db_index=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        verbose_name='Произведение',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        verbose_name='Жанр',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.genre


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Рейтинг не может быть меньше 1'
            ),
            MaxValueValidator(
                10,
                message='Рейтинг не может быть больше 10'
            )
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_field')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        related_name='coments',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['id']
        default_related_name = 'comments'
        verbose_name_plural = 'Коментарии к отзывам'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text
