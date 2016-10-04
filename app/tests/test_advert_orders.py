import json
import jwt
from sqlalchemy import insert
from settings import settings
from aiohttp.test_utils import unittest_run_loop
from extensions.http import StatusCodes
from extensions.testing import BaseTestCase
from routes import EndpointsMapper
from constants import AdvertOrderRanks, ApiErrorCodes
from data_access.advert_orders import advert_orders, AdvertOrdersQueryFactory as AdOrdersQF


class GetAdvertOrdersTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_returns_data_when_authed(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(user_data))
        token = (await response.json())['token']
        owner_id = jwt.decode(token, key=settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])['user_id']
        data = [
            {
                'follow_url_link': 'https://some.link.com',
                'description': 'some_description',
                'heading_picture': 'https://s3.amazon.com/aioads/1232131.jpg',
                'rank': AdvertOrderRanks.LOW,
                'owner_id': owner_id
            },
            {
                'follow_url_link': 'https://website.net',
                'description': 'another description',
                'heading_picture': 'https://s3.amazon.com/aioads/123222.jpg',
                'rank': AdvertOrderRanks.HIGH,
                'owner_id': owner_id
            },
            {
                'follow_url_link': 'https://school.net',
                'description': 'another school description',
                'heading_picture': 'https://s3.amazon.com/aioads/123112.jpg',
                'rank': AdvertOrderRanks.MIDDLE,
                'owner_id': owner_id
            }
        ]
        async with self.test_db_eng.acquire() as conn:
            for order in data:
                await conn.execute(insert(advert_orders).values(**order))

        response = await self.client.get(EndpointsMapper.ADVERT_ORDERS, headers={settings.JWT_HEADER: token})

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert len(body) == 3

        fields_to_check = ('follow_url_link', 'heading_picture', 'description')
        for field in fields_to_check:
            assert body[0][field] == data[1][field]
            assert body[1][field] == data[2][field]
            assert body[2][field] == data[0][field]

        for order in body:
            assert 'id' in order

    @unittest_run_loop
    async def test_returns_401_when_anon(self):
        response = await self.client.get(EndpointsMapper.ADVERT_ORDERS)
        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()


class CreateAdvertOrderTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_creates_order_on_ad_provider_valid_post(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(EndpointsMapper.ADVERT_ORDERS,
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.CREATED
        body = await response.json()
        await response.release()

        assert 'id' in body

        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(AdOrdersQF.get_advert_order_by_id(body['id']))
            data = await rp.first()

        for key, value in order_data.items():
            assert data[key] == value

    @unittest_run_loop
    async def test_returns_400_when_data_is_invalid(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'ht',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(EndpointsMapper.ADVERT_ORDERS,
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'follow_url_link')

    @unittest_run_loop
    async def test_returns_400_when_field_is_missing(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(EndpointsMapper.AD_PROVIDER_SIGNUP, data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(EndpointsMapper.ADVERT_ORDERS,
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_400_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'follow_url_link')

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(EndpointsMapper.ADVERT_ORDERS, data=json.dumps(order_data))
        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()

    @unittest_run_loop
    async def test_returns_403_to_ad_placer(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994',
            'website': 'http://www.somewebsite.com',
            'visitors_per_day_count': 120
        }
        response = await self.client.post(EndpointsMapper.AD_PLACER_SIGNUP, data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(EndpointsMapper.ADVERT_ORDERS,
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.FORBIDDEN
        await response.release()
