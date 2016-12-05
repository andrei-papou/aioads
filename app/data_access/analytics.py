import sqlalchemy as sa
from . import metadata


clicks = sa.Table('clicks', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('placement_id', sa.Integer(), sa.ForeignKey('placements.id'), nullable=False),
    sa.Column('registered_at', sa.DateTime(), nullable=False, server_default=sa.func.now()))


class ClicksQueryFactory:

    @staticmethod
    def create_click(placement_id: int):
        return sa.insert(clicks).values(placement_id=placement_id)
