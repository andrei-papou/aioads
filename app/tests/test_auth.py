import json
import jwt
from aiohttp.test_utils import unittest_run_loop
from sqlalchemy import select
from extensions.testing import BaseTestCase
from extensions.http import StatusCodes
from extensions.user_model import UserTypes
from settings import settings
from constants import ApiErrorCodes, UserTypes
from routes import EndpointsMapper
from data_access.auth import users, ad_placers, ad_providers


class AdPlacerTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_creates_ad_placer_on_valid_post(self):
        data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994',
            'website': 'http://www.somewebsite.com',
            'visitors_per_day_count': 120
        }
        response = await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.CREATED
        body = await response.json()
        await response.release()

        assert 'token' in body

        async with self.test_db_eng.acquire() as conn:
            columns = [users.c.id, users.c.email, ad_placers.c.website, ad_placers.c.visitors_per_day_count]
            tables = users.join(ad_placers, users.c.id == ad_placers.c.user_id)
            query = select(columns).select_from(tables).where(users.c.email == data['email'])

            rp = await conn.execute(query)
            result = await rp.first()

            assert result.email == data['email']
            assert result.website == data['website']
            assert result.visitors_per_day_count == data['visitors_per_day_count']

    @unittest_run_loop
    async def test_returns_400_when_data_is_invalid(self):
        data = {
            'email': 'wrong',
            'password': 'homm1994',
            'website': 'http://www.somewebsite.com',
            'visitors_per_day_count': 120
        }
        response =  await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'email')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()

            assert len(result) == 0

    @unittest_run_loop
    async def test_returns_400_when_field_is_missing(self):
        data = {'password': 'homm1994'}
        response = await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR,
                                     'email', 'website', 'visitors_per_day_count')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()

            assert len(result) == 0

    @unittest_run_loop
    async def test_returns_400_when_email_is_already_in_use(self):
        data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994',
            'website': 'http://www.somewebsite.com',
            'visitors_per_day_count': 120
        }
        await (await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(data))).release()
        response = await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.EMAIL_ALREADY_IN_USE, 'email')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()
            assert len(result) == 1


class AdProviderTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_creates_ad_provider_on_valid_post(self):
        data = {'email': 'popow@gmail.net', 'password': 'somepass'}
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.CREATED
        body = await response.json()
        await response.release()

        assert 'token' in body

        async with self.test_db_eng.acquire() as conn:
            columns = [users.c.email, ad_providers.c.id]
            tables = users.join(ad_providers, users.c.id == ad_providers.c.user_id)
            query = select(columns).select_from(tables).where(users.c.email == data['email'])

            rp = await conn.execute(query)
            result = await rp.first()

            assert 'id' in result
            assert result['email'] == data['email']

    @unittest_run_loop
    async def test_returns_400_when_data_is_invalid(self):
        data = {'email': 'popow@gmail.com', 'password': 'a'}
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'password')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()
            assert len(result) == 0

    @unittest_run_loop
    async def test_returns_400_when_field_is_missing(self):
        data = {'password': 'somepassword'}
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'email')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()
            assert len(result) == 0

    @unittest_run_loop
    async def test_returns_400_when_email_is_already_in_use(self):
        data = {'email': 'valid@email.com', 'password': 'somepassword'}
        json_data = json.dumps(data)
        await (await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json_data)).release()
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json_data)

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.EMAIL_ALREADY_IN_USE, 'email')

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()
            assert len(result) == 1


class LoginTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_logs_in_ad_provider(self):
        data = {'email': 'valid@email.com', 'password': 'somepassword'}
        await (await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))).release()

        data['user_type'] = UserTypes.AD_PROVIDER
        response = await self.client.post(EndpointsMapper.LOGIN, data=json.dumps(data))

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert 'token' in body
        data = jwt.decode(body['token'], settings.JWT_SECRET, settings.JWT_ALGORITHM)
        assert 'user_id' in data
        assert 'type' in data
        assert data['type'] == UserTypes.AD_PROVIDER

    @unittest_run_loop
    async def test_logs_in_ad_placer(self):
        signup_data = {
            'email': 'valid@email.com',
            'website': 'http://www.some.com',
            'password': 'somepassword',
            'visitors_per_day_count': 10
        }
        await (await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(signup_data))).release()

        data = {
            'email': 'valid@email.com',
            'password': 'somepassword',
            'user_type': UserTypes.AD_PLACER
        }
        response = await self.client.post(EndpointsMapper.LOGIN, data=json.dumps(data))

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert 'token' in body
        data = jwt.decode(body['token'], settings.JWT_SECRET, settings.JWT_ALGORITHM)
        assert 'user_id' in data
        assert 'type' in data
        assert data['type'] == UserTypes.AD_PLACER

    @unittest_run_loop
    async def test_returns_400_when_password_is_invalid(self):
        data = {'email': 'valid@email.com', 'password': 'somepassword'}
        await (await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))).release()

        data['password'] = 'dfgjdfkgj'
        data['user_type'] = UserTypes.AD_PROVIDER
        response = await self.client.post(EndpointsMapper.LOGIN, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.PASSWORD_IS_INVALID, 'password')

    @unittest_run_loop
    async def test_returns_400_when_email_does_not_exist(self):
        data = {'email': 'valid@email.com', 'password': 'somepassword'}
        await (await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(data))).release()

        data['email'] = 'someemail@gmail.com'
        data['user_type'] = UserTypes.AD_PROVIDER
        response = await self.client.post(EndpointsMapper.LOGIN, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.USER_DOES_NOT_EXIST, 'email')


class GetAccountDataTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_returns_data_to_authed_user(self):
        signup_data = {
            'email': 'valid@email.com',
            'first_name': 'Andrew',
            'last_name': 'Popov',
            'website': 'http://www.some.com',
            'password': 'somepassword',
            'visitors_per_day_count': 10
        }
        response = await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(signup_data))
        token = (await response.json())['token']
        await response.release()

        response = await self.client.get(EndpointsMapper.GET_USER_DATA, headers={settings.JWT_HEADER: token})

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert body['email'] == signup_data['email']
        assert body['first_name'] == signup_data['first_name']
        assert body['last_name'] == signup_data['last_name']
        assert body['website'] == signup_data['website']
        assert body['visitors_per_day_count'] == signup_data['visitors_per_day_count']

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        response = await self.client.get(EndpointsMapper.GET_USER_DATA)

        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()

    @unittest_run_loop
    async def test_returns_400_when_token_is_invalid(self):
        response = await self.client.get(EndpointsMapper.GET_USER_DATA, headers={settings.JWT_HEADER: 'wrong-token'})

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.AUTH_TOKEN_IS_INVALID, 'token')
