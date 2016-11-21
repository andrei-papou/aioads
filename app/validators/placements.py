from schematics.models import Model
from schematics.types import IntType


class RegisterPlacementValidator(Model):
    order_id = IntType(required=True, min_value=1)
