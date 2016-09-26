from extensions.controllers import BaseController
from extensions.serializers import serialize
from data_access.advert_orders import AdvertOrdersQueryFactory as AdvertOrdersQF
from serialization.advert_orders import list_advert_orders_schema


class AdvertOrdersController(BaseController):

    @serialize(schema=list_advert_orders_schema)
    async def get_orders(self) -> list:
        async with self.db.acquire() as conn:
            rp = await conn.execute(AdvertOrdersQF.get_advert_orders())
        return rp
