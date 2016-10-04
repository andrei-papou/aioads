from sqlalchemy.exc import IntegrityError
from extensions.controllers import BaseController
from extensions.serializers import serialize
from extensions.user_model import User
from data_access.advert_orders import AdvertOrdersQueryFactory as AdvertOrdersQF
from serialization.advert_orders import list_advert_orders_schema
from exceptions.advert_orders import AdvertOrderForSuchLinkAlreadyExists


class AdvertOrdersController(BaseController):

    @serialize(schema=list_advert_orders_schema)
    async def get_orders(self) -> list:
        async with self.db.acquire() as conn:
            rp = await conn.execute(AdvertOrdersQF.get_advert_orders())
        return rp

    async def create_order(self, follow_url_link: str, heading_picture: str, description: str, user: User) -> dict:
        owner_id = user.specific_data['specific_id']
        query = AdvertOrdersQF.create_advert_order(follow_url_link, heading_picture, description, owner_id)
        async with self.db.acquire() as conn:
            try:
                order_id = await conn.scalar(query)
            except IntegrityError:
                raise AdvertOrderForSuchLinkAlreadyExists()
        return {'id': order_id}
