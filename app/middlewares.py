import time
import logging
from settings import settings


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
        request.db = app._db
        return await handler(request)
    return middleware_wrapper


middlewares = (db_middleware, logging_middleware,)
test_middlewares = (db_middleware,)
