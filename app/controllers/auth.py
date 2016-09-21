import jwt
import bcrypt
from psycopg2 import IntegrityError
from settings import settings
from exceptions.auth import EmailAlreadyInUse, WebsiteAlreadyRegistered, UserDoesNotExist, InvalidPassword
from extensions.user_model import UserTypes
from extensions.controllers import BaseController
from data_access.auth import AuthQueryFactory as AuthQF


class AuthController(BaseController):

    def __generate_token(self, user_id, user_type):
        return jwt.encode({'user_id': user_id, 'type': user_type},
                          settings.JWT_SECRET,
                          algorithm=settings.JWT_ALGORITHM).decode('utf8')

    async def __get_signup_base_user_query(self, email: str, password: str, first_name: str = None, last_name: str = None):
        salt = await self.to_thread(bcrypt.gensalt, rounds=settings.SALT_ROUNDS)
        hashed_password = (await self.to_thread(bcrypt.hashpw, password.encode('utf8'), salt)).decode('utf8')

        return AuthQF.insert_base_user(email=email, hashed_password=hashed_password,
                                       first_name=first_name, last_name=last_name)

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
                insert_ad_placer_query = AuthQF.insert_ad_placer_user_part(user_id, website, visitors_per_day_count)
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
                insert_ad_provider_query = AuthQF.insert_ad_provider_user_part(user_id=user_id)
                ad_provider_id = await conn.scalar(insert_ad_provider_query)
            except IntegrityError:
                await trans.rollback()
                # maybe raise some exception but I'm not sure which one

            await trans.commit()

        return self.__generate_token(user_id=ad_provider_id, user_type=UserTypes.AD_PROVIDER)

    async def login(self, email: str, password: str, user_type: str) -> str:

        query = AuthQF.select_user_data_by_email(email=email, user_type=user_type)

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
