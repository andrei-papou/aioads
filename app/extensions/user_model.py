class UserTypes:
    AD_PROVIDER = 'ad-provider'
    AD_PLACER = 'ad-placer'

    @classmethod
    def as_choices(cls):
        return [cls.AD_PROVIDER, cls.AD_PLACER]


class User:
    pass
