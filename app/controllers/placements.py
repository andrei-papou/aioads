from datetime import datetime, timedelta
from collections import Counter
from psycopg2 import IntegrityError
from extensions.db import DatabaseErrors
from extensions.user_model import User
from extensions.controllers import BaseController
from extensions.serializers import serialize
from data_access.placements import PlacementsQueryFactory as PlacementsQF
from serialization.placements import list_placements_schema
from exceptions.analytics import AttemptToGetForeignClicks, AttemptToGetForeignViews
from exceptions.placements import (
    DuplicatedPlacement, AdvertOrderDoesNotExist, PlacementDoesNotExist, AttemptToRemoveForeignPlacement
)
from controllers.mixins import GrabAnalyticsMixin


class PlacementsController(GrabAnalyticsMixin, BaseController):

    async def _get_views_in_date_range(self, user: User, uid: int, start_date: datetime, end_date: datetime):
        check_ownership_query = PlacementsQF.get_placement(uid)
        query = PlacementsQF.get_views(uid, start_date, end_date)
        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            p_data = await rp.first()

            if p_data is None:
                raise PlacementDoesNotExist()

            if p_data.placer_id != user.specific_data['specific_id']:
                raise AttemptToGetForeignViews()

            rp = await conn.execute(query)
        return rp

    async def _get_clicks_in_date_range(self, user: User, uid: int, start_date: datetime, end_date: datetime):
        check_ownership_query = PlacementsQF.get_placement(uid)
        query = PlacementsQF.get_clicks(uid, start_date, end_date)
        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            p_data = await rp.first()

            if p_data is None:
                raise PlacementDoesNotExist()

            if p_data.placer_id != user.specific_data['specific_id']:
                raise AttemptToGetForeignClicks()

            rp = await conn.execute(query)
        return rp

    @serialize(schema=list_placements_schema)
    async def get_placements(self, user: User) -> list:
        query = PlacementsQF.get_placements(user.specific_data['specific_id'])

        async with self.db.acquire() as conn:
            return await conn.execute(query)

    async def create_placement(self, user: User, order_id: int) -> dict:
        query = PlacementsQF.create_placement(user.specific_data['specific_id'], order_id)

        async with self.db.acquire() as conn:
            try:
                pk = await conn.scalar(query)
            except IntegrityError as e:
                code = int(e.pgcode)
                if code == DatabaseErrors.UNIQUE_VIOLATION:
                    raise DuplicatedPlacement()
                elif code == DatabaseErrors.FOREIGN_KEY_VIOLATION:
                    raise AdvertOrderDoesNotExist()

        return {'id': pk}

    async def delete_placement(self, user: User, placement_id: int) -> None:
        check_ownership_query = PlacementsQF.get_placement(placement_id)
        delete_query = PlacementsQF.delete_placement(placement_id)

        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            p_data = await rp.first()

            if p_data is None:
                raise PlacementDoesNotExist()

            if p_data.placer_id != user.specific_data['specific_id']:
                raise AttemptToRemoveForeignPlacement()

            await conn.execute(delete_query)
