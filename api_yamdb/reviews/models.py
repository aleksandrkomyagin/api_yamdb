from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import NAME_MAX_LENGHT, SLUG_MAX_LENGHT
from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=NAME_MAX_LENGHT
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=SLUG_MAX_LENGHT
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
        max_length=NAME_MAX_LENGHT,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=SLUG_MAX_LENGHT
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
        max_length=NAME_MAX_LENGHT
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year],
        db_index=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        related_name='title',
        on_delete=models.SET_NULL,
        null=True,
    )
    description = models.TextField(
        'Описание произведения',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр',
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
        related_name='genre_title_title',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        verbose_name='Жанр',
        related_name='genre_title_genre',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.genre.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews_title',
        verbose_name='произведение'
    )
    text = models.TextField('текст отзыва',)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews_author',
        verbose_name='автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        'оценка',
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
        ordering = ('pub_date',)
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_field')
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='автор комментария',
        related_name='comment_author'
    )
    text = models.TextField('текст',)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        related_name='comment_review',
        on_delete=models.CASCADE,
        verbose_name='отзыв'
    )

    class Meta:
        ordering = ('pub_date',)
        default_related_name = 'comments'
        verbose_name_plural = 'Коментарии к отзывам'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text[:15]
