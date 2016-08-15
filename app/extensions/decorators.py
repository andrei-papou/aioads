import json
from schematics.exceptions import ValidationError, ModelConversionError
from extensions.http import HTTPBadRequest


def validate_body_json(validator):
    def decorator(handler):
        async def wrapper(request, *args):
            try:
                data = await request.json()
            except json.JSONDecodeError:
                return HTTPBadRequest(errors={'general': ['Invalid JSON']})
            try:
                validator(data).validate()
                request.data = data
            except (ValidationError, ModelConversionError) as e:
                return HTTPBadRequest(errors=e.messages)
            return await handler(request, *args)
        return wrapper
    return decorator
