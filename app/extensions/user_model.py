from constants import UserTypes
from data_access.auth import AuthQueryFactory as AuthQF


class User:

    @classmethod
    async def create(cls, db, token_data):
        user_type = token_data['type']
        get_data_query = AuthQF.get_user_data(user_type, token_data['user_id'])
        async with db.acquire() as conn:
            rp = await conn.execute(get_data_query)
            data = await rp.first()
        return User(user_type, data)

    def __init__(self, user_type, data):
        self.id = data.id
        self.email = data.email
        self.first_name = data.first_name
        self.last_name = data.last_name
        self.cash = data.cash
        self.created_at = data.created_at
        self.updated_at = data.updated_at

        self.type = user_type

        self.specific_data = data

    def as_dict(self):
        base = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'cash': self.cash,
        }
        if self.type == UserTypes.AD_PLACER:
            base['website'] = self.specific_data['website']
            base['visitors_per_day_count'] = self.specific_data['visitors_per_day_count']
        else:
            base['is_locked'] = self.specific_data['is_locked']
        return base
