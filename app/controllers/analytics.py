from psycopg2 import IntegrityError
from extensions.controllers import BaseController
from data_access.analytics import ClicksQueryFactory as ClicksQF
from exceptions.analytics import PlacementDoesNotExist


class AnalyticsController(BaseController):

    async def register_click(self, placement_id: int):
        query = ClicksQF.create_click(placement_id)

        async with self.db.acquire() as conn:
            try:
                await conn.execute(query)
            except IntegrityError:
                raise PlacementDoesNotExist()
