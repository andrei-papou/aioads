from asyncio import wrap_future
from concurrent.futures import ThreadPoolExecutor
from settings import settings


class BaseController:
    executor = ThreadPoolExecutor(max_workers=settings.THREAD_POOL_LIMIT)

    def __init__(self, database, app):
        self.db = database
        self.app = app

    async def to_thread(self, func, *args, **kwargs):
        return await wrap_future(self.executor.submit(func, *args, **kwargs), loop=self.app.loop)


def bind_controller(controller_class):
    def decorator(handler):
        async def wrapper(request):
            controller = controller_class(database=request.db, app=request.app)
            return await handler(request, controller)
        return wrapper
    return decorator
