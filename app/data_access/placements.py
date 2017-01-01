from datetime import datetime
import sqlalchemy as sa
from . import metadata
from data_access.analytics import clicks, views


placements = sa.Table('placements', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('placer_id', sa.Integer(), sa.ForeignKey('ad_placers.id'), nullable=False),
    sa.Column('order_id', sa.Integer(), sa.ForeignKey('advert_orders.id'), nullable=False),
    sa.Column('placed_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    sa.UniqueConstraint('placer_id', 'order_id', name='placements_placer_order_uc'))


def get_for_placement(table: sa.Table, p_id: int, start_date: datetime, end_date: datetime):
    return sa.select([table.c.registered_at]).where(sa.and_(
        table.c.placement_id == p_id,
        table.c.registered_at >= start_date,
        table.c.registered_at <= end_date
    ))


class PlacementsQueryFactory:

    @staticmethod
    def get_placements(owner_id: int):
        columns = [
            placements.c.id,
            placements.c.placer_id,
            placements.c.order_id,
            placements.c.placed_at,
            sa.func.count(views.c.id).label('views'),
            sa.func.count(clicks.c.id).label('clicks')
        ]
        tables = placements\
            .outerjoin(clicks, clicks.c.placement_id == placements.c.id)\
            .outerjoin(views, views.c.placement_id == placements.c.id)
        return sa\
            .select(columns)\
            .select_from(tables)\
            .where(placements.c.placer_id == owner_id)\
            .group_by(placements.c.id)

    @staticmethod
    def get_placement(placement_id: int):
        columns = [
            placements.c.id,
            placements.c.placer_id,
            placements.c.order_id,
            placements.c.placed_at,
            sa.func.count(views.c.id).label('views'),
            sa.func.count(clicks.c.id).label('clicks')
        ]
        tables = placements \
            .outerjoin(clicks, clicks.c.placement_id == placements.c.id) \
            .outerjoin(views, views.c.placement_id == placements.c.id)
        return sa \
            .select(columns) \
            .select_from(tables) \
            .where(placements.c.id == placement_id) \
            .group_by(placements.c.id)

    @staticmethod
    def get_clicks(p_id: int, start_date: datetime, end_date: datetime):
        return get_for_placement(clicks, p_id, start_date, end_date)

    @staticmethod
    def get_views(p_id: int, start_date: datetime, end_date: datetime):
        return get_for_placement(views, p_id, start_date, end_date)

    @staticmethod
    def create_placement(placer_id: int, order_id: int):
        data = {'placer_id': placer_id, 'order_id': order_id}
        return sa.insert(placements).values(**data)

    @staticmethod
    def delete_placement(placement_id: int):
        return sa.delete(placements).where(placements.c.id == placement_id)
