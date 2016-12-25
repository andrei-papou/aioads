from datetime import datetime, timedelta
from collections import Counter
from extensions.user_model import User


class GrabAnalyticsMixin:

    async def get_year_views(self, user: User, uid: int, year: int = None) -> dict:
        if year is None:
            year = datetime.now().year

        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        rp = await self._get_views_in_date_range(user, uid, start_date, end_date)
        return dict(Counter([row[0].month for row in rp]))

    async def get_month_views(self, user: User, uid: int, year: int = None, month: int = None):
        now = datetime.now()

        if year is None:
            year = now.year
        if month is None:
            month = now.month

        start_date = datetime(year, month, 1)
        end_date_raw = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        end_date = min(end_date_raw, now)

        rp = await self._get_views_in_date_range(user, uid, start_date, end_date)
        return dict(Counter(row[0].day for row in rp))

    async def get_day_views(self, user: User, uid: int, year: int = None, month: int = None, day: int = None):
        now = datetime.now()

        if year is None:
            year = now.year
        if month is None:
            month = now.month
        if day is None:
            day = now.day

        start_date = datetime(year, month, day, 0)
        end_date = datetime(year, month, day + 1, 0) - timedelta(seconds=1)

        rp = await self._get_views_in_date_range(user, uid, start_date, end_date)
        return dict(Counter(row[0].hour for row in rp))

    async def get_year_clicks(self, user: User, uid: int, year: int = None) -> dict:
        if year is None:
            year = datetime.now().year

        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)

        rp = await self._get_clicks_in_date_range(user, uid, start_date, end_date)
        return dict(Counter([row[0].month for row in rp]))

    async def get_month_clicks(self, user: User, uid: int, year: int = None, month: int = None):
        now = datetime.now()

        if year is None:
            year = now.year
        if month is None:
            month = now.month

        start_date = datetime(year, month, 1)
        end_date_raw = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
        end_date = min(end_date_raw, now)

        rp = await self._get_clicks_in_date_range(user, uid, start_date, end_date)
        return dict(Counter(row[0].day for row in rp))

    async def get_day_clicks(self, user: User, uid: int, year: int = None, month: int = None, day: int = None):
        now = datetime.now()

        if year is None:
            year = now.year
        if month is None:
            month = now.month
        if day is None:
            day = now.day

        start_date = datetime(year, month, day, 0)
        end_date = datetime(year, month, day + 1, 0) - timedelta(seconds=1)

        rp = await self._get_clicks_in_date_range(user, uid, start_date, end_date)
        return dict(Counter(row[0].hour for row in rp))
