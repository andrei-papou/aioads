from sqlalchemy.exc import IntegrityError
from extensions.controllers import BaseController
from extensions.serializers import serialize
from extensions.user_model import User
from data_access.advert_orders import AdvertOrdersQueryFactory as AdvertOrdersQF
from serialization.advert_orders import list_advert_orders_schema
from exceptions.advert_orders import (
    AdvertOrderForSuchLinkAlreadyExists, AnotherUserOrderUpdateAttempt, AdvertOrderDoesNotExist,
    AnotherUserOrderDeleteAttempt
)


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

    async def update_order(self, oid: int, user: User, follow_url_link: str = None,
                           heading_picture: str = None, description: str = None) -> dict:
        data = {
            'follow_url_link': follow_url_link,
            'heading_picture': heading_picture,
            'description': description
        }
        select_order_query = AdvertOrdersQF.get_advert_order_by_id(oid)
        update_order_query = AdvertOrdersQF.update_advert_order(oid, **data)

        async with self.db.acquire() as conn:
            rp = await conn.execute(select_order_query)
            order = await rp.first()

            if order is None:
                raise AdvertOrderDoesNotExist()

            if order.owner_id != user.specific_data['specific_id']:
                raise AnotherUserOrderUpdateAttempt()

            await conn.execute(update_order_query)

        return {'id': oid}

    async def delete_order(self, oid: int, user: User) -> None:
        select_order_query = AdvertOrdersQF.get_advert_order_by_id(oid)
        delete_order_query = AdvertOrdersQF.delete_advert_order(oid)

        async with self.db.acquire() as conn:
            rp = await conn.execute(select_order_query)
            order_data = await rp.first()

            if order_data is None:
                raise AdvertOrderDoesNotExist()

            if order_data.owner_id != user.specific_data['specific_id']:
                raise AnotherUserOrderDeleteAttempt()

            await conn.execute(delete_order_query)
