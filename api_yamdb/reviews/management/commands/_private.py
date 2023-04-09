from reviews.models import Category, Title
from django.db.models.base import ModelBase
from typing import Dict, List
import csv


class ModelLoader:
    def __init__(self,
                 model_class: ModelBase,
                 file_location: str,
                 help: str) -> None:
        self.model_class = model_class
        self.file_location = file_location
        self.help = help

    def load(self):
        with open(self.file_location, 'r', 1, 'utf8') as data_file:
            csvreader = csv.DictReader(data_file, delimiter=',')
            objects_list = []
            for row in csvreader:
                objects_list.append(self.model_class(**row))

            self.model_class.objects.bulk_create(
                objects_list, ignore_conflicts=True)

    def remove(self):
        self.model_class.objects.all().delete()

    def show(self):
        for object in self.model_class.objects.all():
            print(f'{object.pk}:{object}')

    def reload(self):
        self.remove()
        self.load()

    def __str__(self):
        return str(self.model_class.__name__)


class TitleLoader(ModelLoader):
    def __init__(self,
                 titles_file: str,
                 genre_titles_file: str,
                 help: str) -> None:
        self.model_class = Title
        self.titles_file = titles_file
        self.genre_titles_file = genre_titles_file
        self.help = help

    def load(self):
        titles_list = []
        with open(self.titles_file, 'r', 1, 'utf8') as data_file:
            csvreader = csv.DictReader(data_file, delimiter=',')
            for row in csvreader:
                if 'category' in row:
                    row['category'] = Category.objects.get(pk=row['category'])
                titles_list.append(Title(**row))

        Title.objects.bulk_create(titles_list,
                                  ignore_conflicts=True)

        with open(self.genre_titles_file, 'r', 1, 'utf8') as genres_file:
            csvreader = csv.DictReader(genres_file, delimiter=',')
            for row in csvreader:
                title_id = row['title_id']
                genre_id = row['genre_id']
                Title.objects.get(id=title_id).genre.add(genre_id)


class ModelWithFKLoader(ModelLoader):
    def __init__(self,
                 model_class: ModelBase,
                 file_location: str,
                 foreign_keys_map: Dict[str, ModelBase],
                 help: str) -> None:
        self.foreign_keys_map: Dict(str, ModelBase) = foreign_keys_map
        super().__init__(model_class, file_location, help)

    def load(self):
        objects_list = []
        with open(self.file_location, 'r', 1, 'utf8') as data_file:
            csvreader = csv.DictReader(data_file, delimiter=',')
            for row in csvreader:
                for column, model_name in self.foreign_keys_map.items():
                    if column in row:
                        row[column] = model_name.objects.get(
                            pk=int(row[column]))

                objects_list.append(self.model_class(**row))

        self.model_class.objects.bulk_create(objects_list,
                                             ignore_conflicts=True)


def load_models(models: List[ModelLoader]):
    for model in models:
        model.load()


def delete_models(models: List[ModelLoader]):
    for model in models:
        model.remove()
