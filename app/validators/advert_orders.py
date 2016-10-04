from schematics.models import Model
from schematics.types import StringType


class CreateAdvertValidator(Model):
    follow_url_link = StringType(min_length=5, max_length=255, required=True)
    heading_picture = StringType(min_length=5, max_length=255, required=True)
    description = StringType(min_length=3, max_length=4095, required=True)
