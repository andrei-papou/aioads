from extensions.user_model import User
from extensions.controllers import BaseController
from extensions.serializers import serialize
from data_access.placements import PlacementsQueryFactory as PlacementsQF
from serialization.placements import list_placements_schema


class PlacementsController(BaseController):

    serialize(schema=list_placements_schema)
    async def get_placements(self, user: User) -> list:
        query = PlacementsQF.get_placements(user.specific_data['specific_id'])

        async with self.db.acquire() as conn:
            return await conn.execute(query)
