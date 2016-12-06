from datetime import datetime, timedelta
from collections import Counter
from psycopg2 import IntegrityError
from extensions.user_model import User
from extensions.controllers import BaseController
from data_access.analytics import ClicksQueryFactory as ClicksQF, ViewsQueryFactory as ViewsQF
from data_access.placements import PlacementsQueryFactory as PlacementsQF
from exceptions.analytics import PlacementDoesNotExist, AttemptToGetForeignClicks


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

    async def get_year_clicks_for_placement(self, user: User, p_id: int, year: int = None) -> dict:

        if year is None:
            end_date = datetime.now()
            start_date = datetime(end_date.year(), 1, 1)
        else:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        check_ownership_query = PlacementsQF.get_placement(p_id)
        query = ClicksQF.get_clicks_for_placement(p_id, start_date, end_date)
        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            p_data = await rp.first()

            if p_data is None:
                raise PlacementDoesNotExist()

            if p_data.placer_id != user.specific_data['specific_id']:
                raise AttemptToGetForeignClicks()

            rp = await conn.execute(query)
        result = Counter(datetime(date).month for date in rp)

        return dict(result)
