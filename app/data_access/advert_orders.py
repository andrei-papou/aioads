from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.sql import selectable, dml
from constants import AdvertOrderRanks
from data_access.placements import placements
from data_access.analytics import clicks, views
from . import metadata


advert_orders = sa.Table('advert_orders', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('heading_picture', sa.String(255)),
    sa.Column('rank', sa.Integer(), nullable=False, server_default=str(AdvertOrderRanks.LOW)),
    sa.Column('follow_url_link', sa.String(255), unique=True, nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('ad_providers.id'), nullable=False))


def get_for_order(table: sa.Table, o_id: int, start_date: datetime, end_date: datetime):
    tables = advert_orders\
        .outerjoin(placements, advert_orders.c.id == placements.c.order_id)\
        .outerjoin(table, placements.c.id == table.c.placement_id)
    return sa.select([table.c.registered_at]).select_from(tables).where(sa.and_(
        advert_orders.c.id == o_id,
        table.c.registered_at >= start_date,
        table.c.registered_at <= end_date
    ))


class AdvertOrdersQueryFactory:

    @staticmethod
    def get_advert_orders(user_id: int) -> selectable.Select:
        columns = [
            advert_orders.c.id,
            advert_orders.c.heading_picture,
            advert_orders.c.rank,
            advert_orders.c.follow_url_link,
            advert_orders.c.description,
            sa.func.count(clicks.c.id).label('clicks'),
            sa.func.count(views.c.id).label('views')
        ]
        tables = advert_orders\
            .outerjoin(placements, advert_orders.c.id == placements.c.order_id)\
            .outerjoin(views, placements.c.id == views.c.placement_id)\
            .outerjoin(clicks, placements.c.id == clicks.c.placement_id)
        return sa.select(columns)\
            .select_from(tables)\
            .where(advert_orders.c.owner_id == user_id)\
            .group_by(advert_orders.c.id)\
            .order_by(advert_orders.c.rank.desc())

    @staticmethod
    def get_advert_order_by_id(order_id):
        columns = [
            advert_orders.c.id,
            advert_orders.c.heading_picture,
            advert_orders.c.follow_url_link,
            advert_orders.c.rank,
            advert_orders.c.description,
            advert_orders.c.owner_id,
            sa.func.count(clicks.c.id).label('clicks'),
            sa.func.count(views.c.id).label('views')
        ]
        tables = advert_orders \
            .outerjoin(placements, advert_orders.c.id == placements.c.order_id) \
            .outerjoin(views, placements.c.id == views.c.placement_id) \
            .outerjoin(clicks, placements.c.id == clicks.c.placement_id)
        return sa.select(columns) \
            .select_from(tables)\
            .where(advert_orders.c.id == order_id) \
            .group_by(advert_orders.c.id) \
            .order_by(advert_orders.c.rank.desc())

    @staticmethod
    def get_clicks(o_id: int, start_date: datetime, end_date: datetime):
        return get_for_order(clicks, o_id, start_date, end_date)

    @staticmethod
    def get_views(o_id: int, start_date: datetime, end_date: datetime):
        return get_for_order(views, o_id, start_date, end_date)

    @staticmethod
    def create_advert_order(link: str, heading_picture: str, description: str, owner_id: int) -> dml.Insert:
        return sa.insert(advert_orders).values(follow_url_link=link, heading_picture=heading_picture,
                                               description=description, owner_id=owner_id)

    @staticmethod
    def update_advert_order(oid: int, follow_url_link: str = None,
                            heading_picture: str = None, description: str = None) -> dml.Update:
        data_unfiltered = {
            'follow_url_link': follow_url_link,
            'description': description,
            'heading_picture': heading_picture
        }
        return sa.update(advert_orders)\
            .values(**{k: v for k, v in data_unfiltered.items() if v is not None})\
            .where(advert_orders.c.id == oid)

    @staticmethod
    def delete_advert_order(oid: int):
        return sa.delete(advert_orders).where(advert_orders.c.id == oid)
