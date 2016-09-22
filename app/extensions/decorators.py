import json
from schematics.exceptions import ValidationError, ModelConversionError
from extensions.http import HTTPBadRequest, HTTPUnauthorized
from constants import ApiErrorCodes


def validate_body_json(validator):
    def decorator(handler):
        async def wrapper(request, *args):
            try:
                data = await request.json()
            except json.JSONDecodeError:
                return HTTPBadRequest(code=ApiErrorCodes.INVALID_BODY_JSON, errors={'general': ['Invalid JSON']})
            try:
                validator(data).validate()
                request.data = data
            except (ValidationError, ModelConversionError) as e:
                return HTTPBadRequest(code=ApiErrorCodes.BODY_VALIDATION_ERROR, errors=e.messages)
            return await handler(request, *args)
        return wrapper
    return decorator


def auth_required(handler):
    async def wrapper(request, *args):
        if request.user is None:
            return HTTPUnauthorized()
        return await handler(request, *args)
    return wrapper
