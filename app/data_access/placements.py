import sqlalchemy as sa
from . import metadata


placements = sa.Table('placements', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('placer_id', sa.Integer(), sa.ForeignKey('ad_placers.id'), nullable=False),
    sa.Column('order_id', sa.Integer(), sa.ForeignKey('advert_orders.id'), nullable=False),
    sa.Column('placed_at', sa.DateTime(), nullable=False),
    sa.UniqueConstraint('placer_id', 'order_id', name='placements_placer_order_uc'))


class PlacementsQueryFactory:

    @staticmethod
    def get_placements(owner_id):
        columns = [
            placements.c.id,
            placements.c.placer_id,
            placements.c.order_id,
            placements.c.placed_at
        ]
        return sa.select(columns).where(placements.c.placer_id == owner_id)
