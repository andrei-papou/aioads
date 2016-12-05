import json
from aiohttp.test_utils import unittest_run_loop
from extensions.testing import BaseTestCase
from extensions.http import StatusCodes
from routes import EndpointsMapper
from settings import settings
from constants import ApiErrorCodes


class AnalyticsTestCase(BaseTestCase):

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
        self.placer_headers = {settings.JWT_HEADER: token}

        data = {
            'email': 'popow.andrej2008@yandex.ru',
            'password': 'homm1994'
        }
        url = self.app.get_url(EndpointsMapper.AD_PROVIDER_SIGNUP)
        response = await self.client.post(url, data=json.dumps(data))
        self.provider_headers = {settings.JWT_HEADER: (await response.json())['token']}

        order_data = {
            'follow_url_link': 'http://first.link.com',
            'heading_picture': 'http://first.link.com/api',
            'description': 'Some description #1'
        }
        url = self.app.get_url(EndpointsMapper.ADVERT_ORDERS)
        response = await self.client.post(url, headers=self.provider_headers, data=json.dumps(order_data))
        self.order_id = (await response.json())['id']
        await response.release()
        url = self.app.get_url(EndpointsMapper.PLACEMENTS)
        response = await self.client.post(url, headers=self.placer_headers, data=json.dumps({'order_id': self.order_id}))
        self.p_id = (await response.json())['id']
        await response.release()

    @unittest_run_loop
    async def test_click_is_registered_on_placer_post(self):
        url = self.app.get_url(EndpointsMapper.CLICKS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.CREATED
        await response.release()

    @unittest_run_loop
    async def test_returns_400_on_invalid_post(self):
        url = self.app.get_url(EndpointsMapper.CLICKS)
        data = json.dumps({})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()
        self.check_error_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'placement_id')

    @unittest_run_loop
    async def test_returns_400_for_non_existent_placement(self):
        url = self.app.get_url(EndpointsMapper.CLICKS)
        data = json.dumps({'placement_id': self.p_id - 1})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()
        self.check_error_response_body(body, ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST, 'placement_id')

    @unittest_run_loop
    async def test_returns_403_to_ad_provider(self):
        url = self.app.get_url(EndpointsMapper.CLICKS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, headers=self.provider_headers, data=data)

        assert response.status == StatusCodes.FORBIDDEN
        await response.release()

    @unittest_run_loop
    async def test_returns_401_to_anon(self):
        url = self.app.get_url(EndpointsMapper.CLICKS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, data=data)

        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()

    @unittest_run_loop
    async def test_view_is_registered_on_placer_post(self):
        url = self.app.get_url(EndpointsMapper.VIEWS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.CREATED
        await response.release()

    @unittest_run_loop
    async def test_views_returns_400_on_invalid_post(self):
        url = self.app.get_url(EndpointsMapper.VIEWS)
        data = json.dumps({})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()
        self.check_error_response_body(body, ApiErrorCodes.BODY_VALIDATION_ERROR, 'placement_id')

    @unittest_run_loop
    async def test_views_returns_400_for_non_existent_placement(self):
        url = self.app.get_url(EndpointsMapper.VIEWS)
        data = json.dumps({'placement_id': self.p_id - 1})
        response = await self.client.post(url, headers=self.placer_headers, data=data)

        assert response.status == StatusCodes.BAD_REQUEST
        body = await response.json()
        await response.release()
        self.check_error_response_body(body, ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST, 'placement_id')

    @unittest_run_loop
    async def test_views_returns_403_to_ad_provider(self):
        url = self.app.get_url(EndpointsMapper.VIEWS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, headers=self.provider_headers, data=data)

        assert response.status == StatusCodes.FORBIDDEN
        await response.release()

    @unittest_run_loop
    async def test_views_returns_401_to_anon(self):
        url = self.app.get_url(EndpointsMapper.VIEWS)
        data = json.dumps({'placement_id': self.p_id})
        response = await self.client.post(url, data=data)

        assert response.status == StatusCodes.UNAUTHORIZED
        await response.release()
