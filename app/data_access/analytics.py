from datetime import datetime
import sqlalchemy as sa
from . import metadata


clicks = sa.Table('clicks', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('placement_id', sa.Integer(), sa.ForeignKey('placements.id'), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))


views = sa.Table('views', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('placement_id', sa.Integer(), sa.ForeignKey('placements.id'), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))


def get_for_placement(table: sa.Table, p_id: int, start_date: datetime, end_date: datetime):
    return sa.select([table.c.registered_at]).where(sa.and_(
        table.c.placement_id == p_id,
        table.c.registered_at >= start_date,
        table.c.registered_at <= end_date
    ))


class ClicksQueryFactory:

    @staticmethod
    def get_clicks_for_placement(p_id: int, start_date: datetime, end_date: datetime):
        return get_for_placement(clicks, p_id, start_date, end_date)

    @staticmethod
    def create_click(placement_id: int):
        return sa.insert(clicks).values(placement_id=placement_id)


class ViewsQueryFactory:

    @staticmethod
    def get_views_for_placement(p_id: int, start_date: datetime, end_date: datetime):
        return get_for_placement(views, p_id, start_date, end_date)

    @staticmethod
    def create_view(placement_id: int):
        return sa.insert(views).values(placement_id=placement_id)
