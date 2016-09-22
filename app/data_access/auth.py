import sqlalchemy as sa
from sqlalchemy.sql import selectable, dml
from constants import UserTypes
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


class AuthQueryFactory:

    @staticmethod
    def get_user_data(user_type: UserTypes, user_id: int) -> selectable.Select:
        columns = [users]

        if user_type == UserTypes.AD_PLACER:
            join_with = ad_placers
            columns += [ad_placers.c.id.label('specific_id'), ad_placers.c.website, ad_placers.c.visitors_per_day_count]
        else:
            join_with = ad_providers
            columns += [ad_providers.c.id.label('specific_id'), ad_providers.c.is_locked]
        return sa.select(columns)\
            .select_from(users.join(join_with, users.c.id == join_with.c.user_id))\
            .where(join_with.c.id == user_id)

    @staticmethod
    def insert_base_user(email: str, hashed_password: str, first_name: str = None, last_name: str = None) -> dml.Insert:
        data = {'email': email, 'hashed_password': hashed_password}
        if first_name is not None:
            data['first_name'] = first_name
        if last_name is not None:
            data['last_name'] = last_name
        return sa.insert(users).values(**data)

    @staticmethod
    def insert_ad_placer_user_part(user_id: int, website: str, visitors_per_day_count: int) -> dml.Insert:
        data = {'user_id': user_id, 'website': website, 'visitors_per_day_count': visitors_per_day_count}
        return sa.insert(ad_placers).values(**data)

    @staticmethod
    def insert_ad_provider_user_part(user_id: int) -> dml.Insert:
        return sa.insert(ad_providers).values(user_id=user_id)

    @staticmethod
    def select_user_data_by_email(email: str, user_type: str) -> selectable.Select:
        ut_table = (ad_placers if user_type == UserTypes.AD_PLACER else ad_providers)

        tables = ut_table.join(users, ut_table.c.user_id == users.c.id)
        columns = [ut_table.c.id, users.c.hashed_password]

        return sa.select(columns).select_from(tables).where(users.c.email == email)
