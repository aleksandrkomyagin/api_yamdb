from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

CSV_MODELS = {
    # User: 'users.csv',
    # Category: 'category.csv',
    # Genre: 'genre.csv',
    Title: 'titles.csv',
    # GenreTitle: 'genre_title.csv',
    # Review: 'review.csv',
    # Comment: 'comments.csv',
}


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        for model, csv_file in CSV_MODELS.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8'
            ) as file:
                reader = DictReader(file)
                # for r in reader:
                #     r.pop('id', 'Такого ключа нет')
                #     print(r)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
