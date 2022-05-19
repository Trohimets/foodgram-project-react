import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from recipes.models import Ingridient


def ingridient_create(row):
    Ingridient.objects.get_or_create(
        id=row[0],
        title=row[1],
        unit=row[2],
    )

action = {
    'ingredients.csv': ingridient_create,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='+',
            type=str
        )

    def handle(self, *args, **options):
        for filename in options['filename']:
            path = os.path.join(settings.BASE_DIR, "static/data/") + filename
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    action[filename](row)