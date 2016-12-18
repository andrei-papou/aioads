import time
import logging
import jwt
from settings import settings
from constants import ApiErrorCodes
from extensions.user_model import User
from extensions.http import HTTPBadRequest


def get_milliseconds_timestamp():
    return time.time() * 1000

logger = logging.getLogger(settings.LOGGER_NAME)

async def logging_middleware(app, handler):
    async def middleware_wrapper(request):
        start_time = get_milliseconds_timestamp()
        response = await handler(request)
        end_time = get_milliseconds_timestamp()
        logger.debug('[ {method} ] -- {url} -- {time:.2f} ms -- STATUS {status}'.format(
            method=request.method.upper(),
            url=request.path_qs,
            time=end_time - start_time,
            status=response.status
        ))
        return response
    return middleware_wrapper


async def db_middleware(app, handler):
    async def middleware_wrapper(request):
        request.db = app.db
        return await handler(request)
    return middleware_wrapper


async def auth_middleware(app, handler):
    async def middleware_wrapper(request):
        request.user = None
        token = request.headers.get(settings.JWT_HEADER, None)
        if token:
            try:
                payload = jwt.decode(token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return HTTPBadRequest(ApiErrorCodes.AUTH_TOKEN_IS_INVALID, errors={'token': 'Your token is invalid'})
            request.user = await User.create(db=app.db, token_data=payload)
        return await handler(request)
    return middleware_wrapper


async def cors_middleware(app, handler):
    async def middleware_wrapper(request):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '86400'
        return response
    return middleware_wrapper


middlewares = (cors_middleware, db_middleware, logging_middleware, auth_middleware)
test_middlewares = (db_middleware, auth_middleware)
