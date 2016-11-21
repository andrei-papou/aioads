import json
from aiohttp.test_utils import unittest_run_loop
from extensions.testing import BaseTestCase
from extensions.http import StatusCodes
from routes import EndpointsMapper
from settings import settings
from constants import ApiErrorCodes


class GetPlacementsTestCase(BaseTestCase):

    async def set_up(self):
        data = {
            'email': 'popow.andrej2009@yandex.ru',
            'password': 'homm1994',
            'website': 'http://www.somewebsite.com',
            'visitors_per_day_count': 120
        }
        url = self.app.get_url(EndpointsMapper.AD_PLACER_SIGNUP)
        response = await self.client.post(url, data=json.dumps(data))
        token = (await response.json())['token']
        await response.release()
        self.headers = {settings.JWT_HEADER: token}

        data = {
            'email': 'popow.andrej2008@yandex.ru',
            'password': 'homm1994'
        }
        url = self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP)
        response = await self.client.post(url, data=json.dumps(data))
        provider_token = (await response.json())['token']

        order_data = {
            'follow_url_link': 'http://first.link.com',
            'heading_picture': 'http://first.link.com/api',
            'description': 'Some description #1'
        }
        url = self.app.get_url(EndpointsMapper.ADVERT_ORDERS)
        response = await self.client.post(url,
                                          headers={settings.JWT_HEADER: provider_token},
                                          data=json.dumps(order_data))
        self.order_id = (await response.json())['id']
        await response.release()
        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        await self.client.post(url, headers=self.headers, data=json.dumps({'order_id': self.order_id}))

    @unittest_run_loop
    async def test_returns_placement_to_its_owner(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        response = await self.client.get(url, headers=self.headers)

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert len(body) == 1
        assert 'id' in body[0]
        assert body[0]['order_id'] == self.order_id

    @unittest_run_loop
    async def test_returns_nothing_to_not_owner(self):
        other_data = {
            'email': 'popow.andrej20@yandex.ru',
            'password': 'homm1994',
            'website': 'http://www.somewee.com',
            'visitors_per_day_count': 12
        }
        signup_url = self.app.get_url(EndpointsMapper.AD_PLACER_SIGNUP)
        response = await self.client.post(signup_url, data=json.dumps(other_data))
        token = (await response.json())['token']
        await response.release()

        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        response = await self.client.get(url, headers={settings.JWT_HEADER: token})

        assert response.status == StatusCodes.OK
        body = await response.json()
        await response.release()

        assert len(body) == 0

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        response = await self.client.get(self.app.get_url(EndpointsMapper.PLACEMENTS))
        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()

    @unittest_run_loop
    async def test_registers_placement(self):
        """
        Is tested within previous tests and set_up method
        """

    @unittest_run_loop
    async def test_returns_404_for_nonexistent_order(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        response = await self.client.post(url, headers=self.headers, data=json.dumps({'order_id': 1746}))
        assert response.status == StatusCodes.BAD_REQUEST
        await response.release()

    @unittest_run_loop
    async def test_returns_400_for_duplicated_placement(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        response = await self.client.post(url, headers=self.headers, data=json.dumps({'order_id': self.order_id}))
        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()

        assert 'errors' in body
        assert 'order_id' in body['errors']
        assert 'code' in body
        assert body['code'] == ApiErrorCodes.DUPLICATED_PLACEMENT
