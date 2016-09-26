import sqlalchemy as sa
from sqlalchemy.sql import selectable, dml
from constants import AdvertOrderRanks
from . import metadata


advert_orders = sa.Table('advert_orders', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('heading_picture', sa.String(255), unique=True),
    sa.Column('rank', sa.Integer(), nullable=False, server_default=str(AdvertOrderRanks.LOW)),
    sa.Column('follow_url_link', sa.String(255), unique=True, nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('owner_id', sa.Integer(), sa.ForeignKey('ad_providers.id'), nullable=False))


class AdvertOrdersQueryFactory:

    @staticmethod
    def get_advert_orders() -> selectable.Select:
        columns = [
            advert_orders.c.id,
            advert_orders.c.heading_picture,
            advert_orders.c.follow_url_link,
            advert_orders.c.description
        ]
        return sa.select(columns).order_by(advert_orders.c.rank.desc())

    @staticmethod
    def create_advert_order(link: str, description: str, owner_id: int) -> dml.Insert:
        return sa.insert(advert_orders).values(follow_url_link=link, description=description, owner_id=owner_id)

    @staticmethod
    def update_advert_order(oid: int, link: str = None, description: str = None, owner_id: int = None) -> dml.Update:
        data_unfiltered = {'follow_url_link': link, 'description': description, 'owner_id': owner_id}
        return sa.update(advert_orders)\
            .values(**{k: v for k, v in data_unfiltered.items() if v is not None})\
            .where(advert_orders.c.id == oid)
