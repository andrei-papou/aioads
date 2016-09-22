from configparser import ConfigParser


class ApiErrorCodes:
    BODY_VALIDATION_ERROR = 1
    INVALID_BODY_JSON = 2
    EMAIL_ALREADY_IN_USE = 3
    WEBSITE_IS_ALREADY_REGISTERED = 4
    USER_DOES_NOT_EXIST = 5
    PASSWORD_IS_INVALID = 6
    AUTH_TOKEN_IS_INVALID = 7


_config = ConfigParser()
_config.read('messages.ini')
ERROR_MESSAGES = _config['errors']


class UserTypes:
    AD_PROVIDER = 'ad-provider'
    AD_PLACER = 'ad-placer'

    @classmethod
    def as_choices(cls):
        return [cls.AD_PROVIDER, cls.AD_PLACER]