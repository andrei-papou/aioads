import json
from schematics.exceptions import ValidationError, ModelConversionError
from extensions.http import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden
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


def ad_provider_only(handler):
    async def wrapper(request, *args):
        if request.user is None:
            return HTTPUnauthorized()
        if not request.user.is_ad_provider:
            return HTTPForbidden(code=ApiErrorCodes.NOT_AD_PROVIDER, errors={'general': 'You are not an ad provider'})
        return await handler(request, *args)
    return wrapper


def ad_placer_only(handler):
    async def wrapper(request, *args):
        if request.user is None:
            return HTTPUnauthorized()
        if not request.user.is_ad_placer:
            return HTTPForbidden(code=ApiErrorCodes.NOT_AD_PROVIDER, errors={'general': 'You are not an ad provider'})
        return await handler(request, *args)
    return wrapper
