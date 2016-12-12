from calendar import monthrange
from schematics.types import IntType
from schematics.models import Model
from schematics.exceptions import ValidationError
from constants import OLDEST_DATE


class RegisterValidator(Model):
    placement_id = IntType(required=True, min_value=1)


class YearValidator(Model):
    year = IntType(required=False, min_value=OLDEST_DATE.year)


class MonthValidator(YearValidator):
    month = IntType(required=False, min_value=1, max_value=12)


class DayValidator(MonthValidator):
    day = IntType(required=False, min_value=1)

    def validate_day(self, data, value):
        year = data.get('value')
        month = data.get('month')
        day = data.get('day')
        if year and month and day:
            if day > monthrange(year, month):
                raise ValidationError('This month doesn\'t have so many days')


