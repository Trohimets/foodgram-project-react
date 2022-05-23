import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings

from recipes.models import Ingridient, Tag


def tag_create(row):
    Tag.objects.get_or_create(
        title=row[0],
        slug=row[1],
        color=row[2],
    )

def ingridient_create(row):
    Ingridient.objects.get_or_create(
        title=row[0],
        unit=row[1],
    )

action = {
    'ingridients.csv': ingridient_create,
    'tags.csv': tag_create
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