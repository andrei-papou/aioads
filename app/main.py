import logging
import asyncio
from aiohttp import web
from aiopg.sa import create_engine
from middlewares import middlewares
from settings import settings
from routes import route_config
from extensions.app import App


def init_app(loop):
    _db = loop.run_until_complete(create_engine(
        user=settings.DB_USER, database=settings.DB_NAME,
        host=settings.DB_HOST, password=settings.DB_PASS
    ))

    app = App(db=_db, route_config=route_config, middlewares=middlewares)

    logger = logging.getLogger(settings.LOGGER_NAME)
    logger.setLevel(settings.LOGGER_LEVEL)
    sh = logging.StreamHandler()
    sh.setLevel(settings.LOGGER_LEVEL)
    fmtr = logging.Formatter('[ %(asctime)s ] --- [ %(levelname)s ] --- %(message)s')
    sh.setFormatter(fmtr)
    logger.addHandler(sh)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = init_app(loop=loop)
    web.run_app(app, host=settings.HOST, port=settings.PORT)
