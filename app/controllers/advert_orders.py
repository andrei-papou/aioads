from datetime import datetime
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
from controllers.mixins import GrabAnalyticsMixin


class AdvertOrdersController(GrabAnalyticsMixin, BaseController):

    async def _get_views_in_date_range(self, user: User, uid: int, start_date: datetime, end_date: datetime):
        check_ownership_query = AdvertOrdersQF.get_advert_order_by_id(uid)
        query = AdvertOrdersQF.get_views(uid, start_date, end_date)
        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            data = await rp.first()

            if data is None:
                raise AdvertOrderDoesNotExist()

            if data.owner_id != user.specific_data['specific_id']:
                raise AttemptToGetForeignViews()

            rp = await conn.execute(query)
        return rp

    async def _get_clicks_in_date_range(self, user: User, uid: int, start_date: datetime, end_date: datetime):
        check_ownership_query = AdvertOrdersQF.get_advert_order_by_id(uid)
        query = AdvertOrdersQF.get_clicks(uid, start_date, end_date)
        async with self.db.acquire() as conn:
            rp = await conn.execute(check_ownership_query)
            data = await rp.first()

            if data is None:
                raise AdvertOrderDoesNotExist()

            if data.owner_id != user.specific_data['specific_id']:
                raise AttemptToGetForeignClicks()

            rp = await conn.execute(query)
        return rp

    @serialize(schema=list_advert_orders_schema)
    async def get_orders(self) -> list:
        async with self.db.acquire() as conn:
            rp = await conn.execute(AdvertOrdersQF.get_advert_orders())
        return rp

    async def get_order(self, order_id: int) -> dict:
        async with self.db.acquire() as conn:
            rp = await conn.execute(AdvertOrdersQF.get_advert_order_by_id(order_id))
            data = await rp.first()
        if data is None:
            raise AdvertOrderDoesNotExist()
        return {
            'id': data.id,
            'heading_picture': data.heading_picture,
            'follow_url_link': data.follow_url_link,
            'description': data.description,
            'rank': data.rank,
            'clicks': data.clicks,
            'views': data.views
        }

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
