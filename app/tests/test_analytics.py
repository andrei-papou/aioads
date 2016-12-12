import json
from datetime import datetime
from sqlalchemy import insert
from aiohttp.test_utils import unittest_run_loop
from extensions.testing import BaseTestCase
from extensions.http import StatusCodes
from routes import EndpointsMapper
from settings import settings
from constants import ApiErrorCodes
from data_access.analytics import clicks, views


class AnalyticsSetupMixin:

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


class AnalyticsRegisterTestCase(AnalyticsSetupMixin, BaseTestCase):

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


class AnalyticsClicksTestCase(AnalyticsSetupMixin, BaseTestCase):

    async def set_up(self):
        await super().set_up()
        self.now = datetime.now()

        date_range = [
            datetime(self.now.year, 1, 1, 12),
            datetime(self.now.year, 2, 2, 11),
            datetime(self.now.year, self.now.month, 1, 10),
            datetime(self.now.year, self.now.month, 1, 9),
            datetime(self.now.year, self.now.month, 2, 8),
            datetime(self.now.year, self.now.month, self.now.day, 23, 2),
            datetime(self.now.year, self.now.month, self.now.day, 22, 3),
            datetime(self.now.year, self.now.month, self.now.day, 1),
            datetime(2015, 3, 3, 10),
            datetime(2014, 4, 4, 9),
            datetime(2014, 5, 5, 9)
        ]
        async with self.test_db_eng.acquire() as conn:
            for date in date_range:
                await conn.execute(insert(clicks).values(placement_id=self.p_id, registered_at=date))

    @unittest_run_loop
    async def test_placement_year_clicks_returns_default_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_YEAR_CLICKS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 1
        assert '2' in body
        assert body['2'] == 1
        assert str(self.now.month) in body
        assert body[str(self.now.month)] == 6

    @unittest_run_loop
    async def test_placement_year_clicks_returns_param_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_YEAR_CLICKS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 2
        assert '4' in body
        assert body['4'] == 1
        assert '5' in body
        assert body['5'] == 1

    @unittest_run_loop
    async def test_placement_month_clicks_returns_default_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_MONTH_CLICKS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 2
        assert '2' in body
        assert body['2'] == 1

    @unittest_run_loop
    async def test_placement_month_clicks_returns_param_year_and_month(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_MONTH_CLICKS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014, 'month': 4})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 1
        assert '4' in body
        assert body['4'] == 1

    @unittest_run_loop
    async def test_placement_day_clicks_returns_default_day_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_DAY_CLICKS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 1
        assert '22' in body
        assert body['22'] == 1
        assert '23' in body
        assert body['23'] == 1

    @unittest_run_loop
    async def test_placement_day_clicks_returns_param_day_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_DAY_CLICKS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014, 'month': 5, 'day': 5})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 1
        assert '9' in body
        assert body['9'] == 1


class AnalyticsViewsTestCase(AnalyticsSetupMixin, BaseTestCase):

    async def set_up(self):
        await super().set_up()
        self.now = datetime.now()

        date_range = [
            datetime(self.now.year, 1, 1, 12),
            datetime(self.now.year, 2, 2, 11),
            datetime(self.now.year, self.now.month, 1, 10),
            datetime(self.now.year, self.now.month, 1, 9),
            datetime(self.now.year, self.now.month, 2, 8),
            datetime(self.now.year, self.now.month, self.now.day, 23, 2),
            datetime(self.now.year, self.now.month, self.now.day, 22, 3),
            datetime(self.now.year, self.now.month, self.now.day, 1),
            datetime(2015, 3, 3, 10),
            datetime(2014, 4, 4, 9),
            datetime(2014, 5, 5, 9)
        ]
        async with self.test_db_eng.acquire() as conn:
            for date in date_range:
                await conn.execute(insert(views).values(placement_id=self.p_id, registered_at=date))

    @unittest_run_loop
    async def test_placement_year_views_returns_default_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_YEAR_VIEWS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 1
        assert '2' in body
        assert body['2'] == 1
        assert str(self.now.month) in body
        assert body[str(self.now.month)] == 6

    @unittest_run_loop
    async def test_placement_year_views_returns_param_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_YEAR_VIEWS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 2
        assert '4' in body
        assert body['4'] == 1
        assert '5' in body
        assert body['5'] == 1

    @unittest_run_loop
    async def test_placement_month_views_returns_default_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_MONTH_VIEWS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 2
        assert '2' in body
        assert body['2'] == 1

    @unittest_run_loop
    async def test_placement_month_views_returns_param_year_and_month(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_MONTH_VIEWS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014, 'month': 4})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 1
        assert '4' in body
        assert body['4'] == 1

    @unittest_run_loop
    async def test_placement_day_views_returns_default_day_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_DAY_VIEWS, parts={'placement_id': self.p_id})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 3
        assert '1' in body
        assert body['1'] == 1
        assert '22' in body
        assert body['22'] == 1
        assert '23' in body
        assert body['23'] == 1

    @unittest_run_loop
    async def test_placement_day_views_returns_param_day_month_and_year_data(self):
        url = self.app.get_url(EndpointsMapper.PLACEMENT_DAY_VIEWS,
                               parts={'placement_id': self.p_id},
                               query={'year': 2014, 'month': 5, 'day': 5})
        response = await self.client.get(url, headers=self.placer_headers)

        body = await response.json()
        await response.release()

        assert len(body) == 1
        assert '9' in body
        assert body['9'] == 1
