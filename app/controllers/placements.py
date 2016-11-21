from psycopg2 import IntegrityError
from extensions.db import DatabaseErrors
from extensions.user_model import User
from extensions.controllers import BaseController
from extensions.serializers import serialize
from data_access.placements import PlacementsQueryFactory as PlacementsQF
from serialization.placements import list_placements_schema
from exceptions.placements import DuplicatedPlacement, AdvertOrderDoesNotExist


class PlacementsController(BaseController):

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
