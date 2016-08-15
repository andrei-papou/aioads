import jwt
import bcrypt
from psycopg2 import IntegrityError
from sqlalchemy import select, insert
from settings import settings
from exceptions.auth import EmailAlreadyInUse, WebsiteAlreadyRegistered, UserDoesNotExist, InvalidPassword
from extensions.user_model import UserTypes
from extensions.controllers import BaseController
from data_access.auth import ad_placers, users, ad_providers


class AuthController(BaseController):

    #############################  SQL Queries  #############################

    def __sql_insert_base_user(self, email: str, hashed_password: str, first_name: str = None, last_name: str = None):
        data = {'email': email, 'hashed_password': hashed_password}
        if first_name is not None:
            data['first_name'] = first_name
        if last_name is not None:
            data['last_name'] = last_name
        return insert(users).values(**data)

    def __sql_insert_ad_placer_user_part(self, user_id: int, website: str, visitors_per_day_count: int):
        data = {'user_id': user_id, 'website': website, 'visitors_per_day_count': visitors_per_day_count}
        return insert(ad_placers).values(**data)

    def __sql_insert_ad_provider_user_part(self, user_id: int):
        return insert(ad_providers).values(user_id=user_id)

    def __sql_select_user_data_by_email(self, email: str, user_type: str):
        ut_table = (ad_placers if user_type == UserTypes.AD_PLACER else ad_providers)

        tables = ut_table.join(users, ut_table.c.user_id == users.c.id)
        columns = [ut_table.c.id, users.c.hashed_password]

        return select(columns).select_from(tables).where(users.c.email == email)

    #############################  Private methods  #############################

    def __generate_token(self, user_id, user_type):
        return jwt.encode({'user_id': user_id, 'type': user_type},
                          settings.JWT_SECRET,
                          algorithm=settings.JWT_ALGORITHM).decode('utf8')

    async def __get_signup_base_user_query(self, email: str, password: str, first_name: str = None, last_name: str = None):
        salt = await self.to_thread(bcrypt.gensalt, rounds=settings.SALT_ROUNDS)
        hashed_password = (await self.to_thread(bcrypt.hashpw, password.encode('utf8'), salt)).decode('utf8')

        insert_user_base_query = self.__sql_insert_base_user(email=email, hashed_password=hashed_password,
                                                             first_name=first_name, last_name=last_name)
        return insert_user_base_query

    #############################  Public API  #############################

    async def signup_ad_placer(self, email: str, password: str, website: str,
                               visitors_per_day_count: int, first_name: str = None, last_name: str = None) -> str:
        insert_user_base_query = await self.__get_signup_base_user_query(email=email, password=password,
                                                                         first_name=first_name, last_name=last_name)

        async with self.db.acquire() as conn:
            trans = await conn.begin()

            try:
                user_id = await conn.scalar(insert_user_base_query)
            except IntegrityError:
                await trans.rollback()
                raise EmailAlreadyInUse()
            try:
                insert_ad_placer_query = self.__sql_insert_ad_placer_user_part(user_id, website, visitors_per_day_count)
                ad_placer_id = await conn.scalar(insert_ad_placer_query)
            except IntegrityError:
                await trans.rollback()
                raise WebsiteAlreadyRegistered()

            await trans.commit()

        return self.__generate_token(user_id=ad_placer_id, user_type=UserTypes.AD_PLACER)

    async def signup_ad_provider(self, email: str, password: str, first_name: str = None, last_name: str = None) -> str:
        insert_user_base_query = await self.__get_signup_base_user_query(email=email, password=password,
                                                                         first_name=first_name, last_name=last_name)

        async with self.db.acquire() as conn:
            trans = await conn.begin()

            try:
                user_id = await conn.scalar(insert_user_base_query)
            except IntegrityError:
                await trans.rollback()
                raise EmailAlreadyInUse()
            try:
                insert_ad_provider_query = self.__sql_insert_ad_provider_user_part(user_id=user_id)
                ad_provider_id = await conn.scalar(insert_ad_provider_query)
            except IntegrityError:
                await trans.rollback()
                # maybe raise some exception but I'm not sure which one

            await trans.commit()

        return self.__generate_token(user_id=ad_provider_id, user_type=UserTypes.AD_PROVIDER)

    async def login(self, email: str, password: str, user_type: str) -> str:

        query = self.__sql_select_user_data_by_email(email=email, user_type=user_type)

        async with self.db.acquire() as conn:
            rp = await conn.execute(query)
            result = await rp.first()
            if result is None:
                raise UserDoesNotExist()
            right_hashed_pw = result.hashed_password

        try:
            hashed_pw = (await self.to_thread(bcrypt.hashpw,
                                              password.encode('utf8'),
                                              right_hashed_pw.encode('utf8'))).decode('utf8')
        except ValueError:
            raise InvalidPassword()

        if hashed_pw != right_hashed_pw:
            raise InvalidPassword()

        return self.__generate_token(user_id=result.id, user_type=user_type)
