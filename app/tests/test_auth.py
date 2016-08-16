import json
from aiohttp.test_utils import unittest_run_loop
from sqlalchemy import select
from extensions.testing import BaseTestCase
from extensions.http import StatusCodes
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

        assert 'errors' in body
        assert 'email' in body['errors']

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

        assert 'errors' in body
        assert 'email' in body['errors']
        assert 'website' in body['errors']
        assert 'visitors_per_day_count' in body['errors']

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

        assert 'errors' in body
        assert 'email' in body['errors']

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

        assert 'errors' in body
        assert 'password' in body['errors']

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

        assert 'errors' in body
        assert 'email' in body['errors']

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

        assert 'errors' in body
        assert 'email' in body['errors']

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select([users]))
            result = await rp.fetchall()
            assert len(result) == 1
