from datetime import datetime

from django.core.exceptions import ValidationError

MINIMUM_TITLE_YEAR = -500000  # The first known work of art


def validate_creation_year(value):
    if value < MINIMUM_TITLE_YEAR or value > datetime.now().year:
        raise ValidationError(
            f'The year value must be between {MINIMUM_TITLE_YEAR}'
            f' and {datetime.now().year}')
