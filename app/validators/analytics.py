from schematics.types import IntType
from schematics.models import Model
from constants import OLDEST_DATE


class RegisterValidator(Model):
    placement_id = IntType(required=True, min_value=1)


class YearValidator(Model):
    year = IntType(required=False, min_value=OLDEST_DATE.year)


class MonthValidator(YearValidator):
    month = IntType(required=False, min_value=1, max_value=12)
