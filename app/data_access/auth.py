import sqlalchemy as sa
from . import metadata


users = sa.Table('users', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('email', sa.String(255), unique=True, nullable=False),
    sa.Column('hashed_password', sa.String(255), nullable=False),
    sa.Column('first_name', sa.String(255)),
    sa.Column('last_name', sa.String(255)),
    sa.Column('cash', sa.Float(), server_default='0'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.func.current_timestamp()))


ad_providers = sa.Table('ad_providers', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    sa.Column('is_locked', sa.Boolean(), server_default='0'))


ad_placers = sa.Table('ad_placers', metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
    sa.Column('website', sa.String(), nullable=False),
    sa.Column('visitors_per_day_count', sa.Integer(), nullable=False))
