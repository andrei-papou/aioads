from datetime import datetime, timedelta
from collections import Counter
from psycopg2 import IntegrityError
from extensions.user_model import User
from extensions.controllers import BaseController
from data_access.analytics import ClicksQueryFactory as ClicksQF, ViewsQueryFactory as ViewsQF
from data_access.placements import PlacementsQueryFactory as PlacementsQF
from exceptions.analytics import PlacementDoesNotExist, AttemptToGetForeignClicks, AttemptToGetForeignViews


class AnalyticsController(BaseController):

    async def register_click(self, placement_id: int):
        query = ClicksQF.create_click(placement_id)

        async with self.db.acquire() as conn:
            try:
                await conn.execute(query)
            except IntegrityError:
                raise PlacementDoesNotExist()

    async def register_view(self, placement_id: int):
        query = ViewsQF.create_view(placement_id)

        async with self.db.acquire() as conn:
            try:
                await conn.execute(query)
            except IntegrityError:
                raise PlacementDoesNotExist()
