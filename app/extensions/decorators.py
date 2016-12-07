import json
from schematics.exceptions import ValidationError, ModelConversionError
from extensions.http import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden
from constants import ApiErrorCodes


def validate_body_json(validator, kw_name='body'):
    def decorator(handler):
        async def wrapper(request, *args, **kwargs):
            try:
                data = await request.json()
            except json.JSONDecodeError:
                return HTTPBadRequest(code=ApiErrorCodes.INVALID_BODY_JSON, errors={'general': ['Invalid JSON']})
            try:
                v = validator(data)
                v.validate()
                kwargs[kw_name] = v.to_native()
            except (ValidationError, ModelConversionError) as e:
                return HTTPBadRequest(code=ApiErrorCodes.BODY_VALIDATION_ERROR, errors=e.messages)
            return await handler(request, *args, **kwargs)
        return wrapper
    return decorator


def parse_query_params(validator, kw_name='params'):
    def decorator(handler):
        async def wrapper(request, *args, **kwargs):
            data = {}
            if request.query_string:
                try:
                    data = dict(pair.split('=') for pair in request.query_string.split('&'))
                except ValueError:
                    return HTTPBadRequest(code=ApiErrorCodes.QUERY_PARAMS_INVALID_FORMAT,
                                          errors={'general': 'invalid query params format'})
            try:
                v = validator(data)
                v.validate()
                kwargs[kw_name] = v.to_native()
            except (ValidationError, ModelConversionError) as e:
                return HTTPBadRequest(code=ApiErrorCodes.QUERY_PARAMS_VALIDATION_ERROR, errors=e.messages)
            return await handler(request, *args, **kwargs)
        return wrapper
    return decorator


def auth_required(handler):
    async def wrapper(request, *args, **kwargs):
        if request.user is None:
            return HTTPUnauthorized()
        return await handler(request, *args, **kwargs)
    return wrapper


def ad_provider_only(handler):
    async def wrapper(request, *args, **kwargs):
        if request.user is None:
            return HTTPUnauthorized()
        if not request.user.is_ad_provider:
            return HTTPForbidden(code=ApiErrorCodes.NOT_AD_PROVIDER, errors={'general': 'You are not an ad provider'})
        return await handler(request, *args, **kwargs)
    return wrapper


def ad_placer_only(handler):
    async def wrapper(request, *args, **kwargs):
        if request.user is None:
            return HTTPUnauthorized()
        if not request.user.is_ad_placer:
            return HTTPForbidden(code=ApiErrorCodes.NOT_AD_PROVIDER, errors={'general': 'You are not an ad provider'})
        return await handler(request, *args, **kwargs)
    return wrapper
