from asyncio import wrap_future
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from settings import settings


class BaseController:
    thread_executor = ThreadPoolExecutor(max_workers=settings.THREAD_POOL_LIMIT)
    process_executor = ProcessPoolExecutor(max_workers=settings.PROCESS_POOL_LIMIT)

    def __init__(self, database, app):
        self.db = database
        self.app = app

    async def to_thread(self, func, *args, **kwargs):
        return await wrap_future(self.thread_executor.submit(func, *args, **kwargs), loop=self.app.loop)

    async def to_process(self, func, *args, **kwargs):
        return await wrap_future(self.process_executor.submit(func, *args, **kwargs), loop=self.app.loop)


def bind_controller(controller_class, kw_name = 'controller'):
    def decorator(handler):
        async def wrapper(request, *args, **kwargs):
            controller = controller_class(database=request.db, app=request.app)
            kwargs[kw_name] = controller
            return await handler(request, *args, **kwargs)
        return wrapper
    return decorator
