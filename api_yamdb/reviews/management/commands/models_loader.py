from ._private import (ModelLoader,
                       TitleLoader,
                       ModelWithFKLoader,
                       load_models,
                       delete_models)
from django.core.management.base import (BaseCommand,
                                         CommandParser,
                                         CommandError)
from reviews.models import Category, Genre, Title, Review, Comment
import pathlib
from django.contrib.auth import get_user_model
from typing import Dict
User = get_user_model()


class Command(BaseCommand):

    base_data_file_location = (pathlib.Path().absolute() / 'api_yamdb'
                               / "static"
                               / "data")

    loaders_dict: Dict[str, ModelLoader] = {
        "user": ModelLoader(User,
                            base_data_file_location / "users.csv",
                            "Load Users"),

        "category": ModelLoader(Category,
                                base_data_file_location / "category.csv",
                                "Load Categories"),

        "genre": ModelLoader(Genre,
                             base_data_file_location / "genre.csv",
                             "Load Genres"),

        "title": TitleLoader(base_data_file_location / "titles.csv",
                             base_data_file_location / "genre_title.csv",
                             "Load Titles"),

        "review": ModelWithFKLoader(Review,
                                    base_data_file_location / "review.csv",
                                    {"title": Title, 'author': User},
                                    "Load Reviews"),

        "comment": ModelWithFKLoader(Comment,
                                     base_data_file_location / "comments.csv",
                                     {"review": Review, 'author': User},
                                     "Load Comments"),


    }

    creation_order = [
        'user',
        'category',
        'genre',
        'title',
        'review',
        'comment'
    ]

    def add_arguments(self, parser: CommandParser):

        parser.add_argument('--all',
                            action='store_true',
                            help='Flag for operations with all models')

        parser.add_argument('--load',
                            action='store_true',
                            help='Load all data for model from file')
        parser.add_argument('--show',
                            action='store_true',
                            help='Show all model instances')
        parser.add_argument('--delete',
                            action='store_true',
                            help='Delete all model instances')
        parser.add_argument('--reload',
                            action='store_true',
                            help='Reload all model instances')

        for command, loader in self.loaders_dict.items():
            parser.add_argument(f'--{command}',
                                action='store_true',
                                help=loader)

    def process_all_models(self, options):
        creation_loaders = [self.loaders_dict[model_name]
                            for model_name in self.creation_order]
        removing_loaders = list(creation_loaders)
        removing_loaders.reverse()

        if options['load']:
            load_models(creation_loaders)
            return

        if options['delete']:
            delete_models(removing_loaders)
            return

        if options['reload']:
            delete_models(removing_loaders)
            load_models(creation_loaders)
            return

        raise CommandError(
            "Action is not set. Use one of [--load, --delete, --reload]")

    def process_inividual_model(self, options):
        model_loader = None
        for command in self.loaders_dict.keys():
            if options[command]:
                model_loader = self.loaders_dict[command]
                break
        if not model_loader:
            raise CommandError(
                ('Loader not found, you should use one'
                 f'of {self.loaders_dict.keys()} values'))

        if options['load']:
            model_loader.load()
            return

        if options['show']:
            model_loader.show()
            return

        if options['delete']:
            model_loader.remove()
            return

        if options['reload']:
            model_loader.reload()
            return

        raise CommandError(
            "Command is not set. Use one of"
            " [--load, --show, --delete, --reload]")

    def handle(self, *args, **options):

        if options['all']:
            self.process_all_models(options)
            return

        self.process_inividual_model(options)
