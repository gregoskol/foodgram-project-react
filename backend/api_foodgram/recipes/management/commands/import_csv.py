import csv
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient  # isort:skip


def import_ingredient(model, reader):
    records = [
        model(
            name=row[0],
            measurement_unit=row[1],
        )
        for row in reader
    ]
    model.objects.bulk_create(records)
    print(f"Импорт в модель {model.__name__} завершен")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-fn",
            "--file_name",
            type=str,
            help="Введите название базы - файл.csv",
        )
        parser.add_argument(
            "-mn", "--model_name", type=str, help="Введите название модели"
        )

    def handle(self, *args, **options):
        print(settings.BASE_DIR)
        self.file_path = os.path.join(
            settings.BASE_DIR, "static/data", options["file_name"]
        )
        self.name_model = options["model_name"]
        self.model = apps.get_model("recipes", self.name_model)
        csv_file = open(self.file_path, "r", encoding="utf-8")
        reader = csv.reader(csv_file, delimiter=",")
        next(reader, None)
        models_func = {
            Ingredient: import_ingredient,
        }
        for model, func in models_func.items():
            if self.model is model:
                print(f"Выполняется импорт из {self.file_path}")
                func(self.model, reader)
