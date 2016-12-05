from schematics.types import IntType
from schematics.models import Model


class RegisterClickValidator(Model):
    placement_id = IntType(required=True, min_value=1)
