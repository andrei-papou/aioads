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
        url = self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP)
        response = await self.client.post(url, data=json.dumps(user_data))
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

        url = self.app.get_url(EndpointsMapper.ADVERT_ORDERS)
        response = await self.client.get(url, headers={settings.JWT_HEADER: token})

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
        response = await self.client.get(self.app.get_url(EndpointsMapper.ADVERT_ORDERS))
        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()


class CreateAdvertOrderTestCase(BaseTestCase):

    @unittest_run_loop
    async def test_creates_order_on_ad_provider_valid_post(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        url = self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP)
        response = await self.client.post(url, data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
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
        response = await self.client.post(self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'ht',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_error_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'follow_url_link')

    @unittest_run_loop
    async def test_returns_400_when_field_is_missing(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_error_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'follow_url_link')

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          data=json.dumps(order_data))
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
        response = await self.client.post(self.app.get_url(EndpointsMapper.AD_PLACER_SIGNUP),
                                          data=json.dumps(user_data))
        token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          headers={settings.JWT_HEADER: token},
                                          data=json.dumps(order_data))
        assert response.status == StatusCodes.FORBIDDEN
        await response.release()


class UpdateAdvertOrderTestCase(BaseTestCase):

    async def set_up(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        self.headers = {settings.JWT_HEADER: (await response.json())['token']}
        self.data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          data=json.dumps(self.data), headers=self.headers)
        self.oid = (await response.json())['id']

    @property
    def url(self):
        return self.app.get_url(EndpointsMapper.ADVERT_ORDER, parts={'order_id': self.oid})

    @property
    async def db_data(self):
        select_order_query = AdOrdersQF.get_advert_order_by_id(self.oid)
        async with self.test_db_eng.acquire() as conn:
            rp = await conn.execute(select_order_query)
            return await rp.first()

    @unittest_run_loop
    async def test_updates_order_on_owner_valid_post(self):
        data = {'heading_picture': 'https://www.cdn.class.com/new_promo_cover_image'}
        response = await self.client.patch(self.url, headers=self.headers, data=json.dumps(data))

        assert response.status == StatusCodes.OK
        await response.release()

        assert (await self.db_data)['heading_picture'] == data['heading_picture']

    @unittest_run_loop
    async def test_returns_400_when_order_not_exist(self):
        data = {'heading_picture': 'https://www.cdn.class.com/new_promo_cover_image'}
        url = self.app.get_url(EndpointsMapper.ADVERT_ORDER, parts={'order_id': self.oid + 1})
        response = await self.client.patch(url, headers=self.headers, data=json.dumps(data))

        assert response.status == StatusCodes.NOT_FOUND
        await response.release()

    @unittest_run_loop
    async def test_returns_400_on_invalid_owner_post(self):
        data = {'heading_picture': 'h'}
        response = await self.client.patch(self.url, headers=self.headers, data=json.dumps(data))

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        self.check_error_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'heading_picture')

    @unittest_run_loop
    async def test_returns_403_on_another_user_post(self):
        user_data = {
            'email': 'andrei1111@tut.by',
            'password': 'homm1994'
        }
        response = await self.client.post(path=self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        headers = {settings.JWT_HEADER: (await response.json())['token']}
        data = {'heading_picture': 'https://www.cdn.class.com/new_promo_cover_image'}
        response = await self.client.patch(self.url, headers=headers, data=json.dumps(data))

        assert response.status == StatusCodes.FORBIDDEN
        body = await response.json()
        await response.release()

        self.check_error_response_body(body, ApiErrorCodes.ANOTHER_USER_ORDER_UPDATE_ATTEMPT, 'order_id')
        assert (await self.db_data)['heading_picture'] == self.data['heading_picture']

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        data = {'heading_picture': 'https://www.cdn.class.com/new_promo_cover_image'}
        response = await self.client.patch(self.url, data=json.dumps(data))

        assert response.status == StatusCodes.UNAUTHORIZED
        assert (await self.db_data)['heading_picture'] == self.data['heading_picture']


class DeleteAdvertOrderTestCase(BaseTestCase):

    async def set_up(self):
        user_data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        self.headers = {settings.JWT_HEADER: (await response.json())['token']}
        self.data = {
            'follow_url_link': 'https://www.class.com/index',
            'heading_picture': 'https://www.cdn.class.com/promo_cover_image',
            'description': 'Some description text'
        }
        response = await self.client.post(self.app.get_url(EndpointsMapper.ADVERT_ORDERS),
                                          data=json.dumps(self.data), headers=self.headers)
        self.oid = (await response.json())['id']

    async def check_order_exists_in_db(self):
        get_order_query = AdOrdersQF.get_advert_order_by_id(order_id=self.oid)
        async with self.test_db_eng.acquire() as conn:
            row = await conn.scalar(get_order_query)
            assert row is not None

    @property
    def url(self):
        return self.app.get_url(EndpointsMapper.ADVERT_ORDER, parts={'order_id': self.oid})

    @unittest_run_loop
    async def test_deletes_order_on_owner_delete(self):
        response = await self.client.delete(self.url, headers=self.headers)

        assert response.status == StatusCodes.NO_CONTENT
        await response.release()

        get_order_query = AdOrdersQF.get_advert_order_by_id(order_id=self.oid)
        async with self.test_db_eng.acquire() as conn:
            row = await conn.scalar(get_order_query)
            assert row is None

    @unittest_run_loop
    async def test_returns_404_if_order_not_exist(self):
        url = self.app.get_url(EndpointsMapper.ADVERT_ORDER, parts={'order_id': self.oid + 1})
        response = await self.client.delete(url, headers=self.headers)

        assert response.status == StatusCodes.NOT_FOUND
        await response.release()

    @unittest_run_loop
    async def test_returns_403_to_another_user(self):
        user_data = {
            'email': 'andrei1111@tut.by',
            'password': 'homm1994'
        }
        response = await self.client.post(path=self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP),
                                          data=json.dumps(user_data))
        headers = {settings.JWT_HEADER: (await response.json())['token']}

        response = await self.client.delete(self.url, headers=headers)

        assert response.status == StatusCodes.FORBIDDEN
        body = await response.json()
        await response.release()

        self.check_error_response_body(body, ApiErrorCodes.ANOTHER_USER_ORDER_DELETE_ATTEMPT, 'order_id')
        await self.check_order_exists_in_db()

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        response = await self.client.delete(self.url)

        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()

        await self.check_order_exists_in_db()
