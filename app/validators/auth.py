from schematics.models import Model
from schematics.types import StringType, IntType
from constants import UserTypes
from .common import WEBSITE_REGEX


EMAIL_REGEX = r'[a-zA-Z0-9\._-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$'


class LoginValidator(Model):
    email = StringType(regex=EMAIL_REGEX, max_length=255, required=True)
    password = StringType(required=True)
    user_type = StringType(choices=UserTypes.as_choices(), required=True)


class SignupValidator(Model):
    email = StringType(regex=EMAIL_REGEX, max_length=255, required=True)
    password = StringType(required=True, min_length=3)
    first_name = StringType(max_length=255)
    last_name = StringType(max_length=255)


class AdPlacerSignupValidator(SignupValidator):
    website = StringType(regex=WEBSITE_REGEX, max_length=255, required=True)
    visitors_per_day_count = IntType(required=True)


class AdProviderSignupValidator(SignupValidator):
    pass
