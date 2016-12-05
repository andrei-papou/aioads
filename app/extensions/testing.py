from aiohttp.test_utils import AioHTTPTestCase
from aiopg.sa import create_engine
from sqlalchemy import text
from middlewares import test_middlewares
from routes import route_config
from settings import settings
from .app import App


class BaseTestCase(AioHTTPTestCase):

    async def set_up(self):
        pass

    async def tear_down(self):
        pass

    def get_app(self, loop):
        _db = loop.run_until_complete(create_engine(
            user=settings.TEST_DB_USER, database=settings.TEST_DB_NAME,
            host=settings.TEST_DB_HOST, password=settings.TEST_DB_PASS,
            loop=loop
        ))

        app = App(db=_db, loop=loop, route_config=route_config, middlewares=test_middlewares)

        self.test_db_eng = app.db

        return app

    async def reset_db(self):
        """
        Query should be updated as soon as new DB changes introduced by tests should be rolled back.
        """
        async with self.test_db_eng.acquire() as conn:
            await conn.execute(text("""
                DELETE FROM clicks;
                DELETE FROM placements;
                DELETE FROM advert_orders;
                DELETE FROM ad_placers;
                DELETE FROM ad_providers;
                DELETE FROM users;
            """))

    def setUp(self):
        super().setUp()
        self.loop.run_until_complete(self.set_up())

    def tearDown(self):
        self.loop.run_until_complete(self.tear_down())
        self.loop.run_until_complete(self.reset_db())
        super().tearDown()

    def check_error_response_body(self, body, code, *invalid_fields):
        assert 'code' in body
        assert body['code'] == code
        assert 'errors' in body
        for field in invalid_fields:
            assert field in body['errors']
