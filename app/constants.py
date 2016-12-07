from datetime import datetime
from configparser import ConfigParser


class ApiErrorCodes:
    BODY_VALIDATION_ERROR = 1
    INVALID_BODY_JSON = 2
    EMAIL_ALREADY_IN_USE = 3
    WEBSITE_IS_ALREADY_REGISTERED = 4
    USER_DOES_NOT_EXIST = 5
    PASSWORD_IS_INVALID = 6
    AUTH_TOKEN_IS_INVALID = 7
    AD_ORDER_FOR_LINK_EXISTS = 8
    NOT_AD_PROVIDER = 9
    NOT_AD_PLACER = 10
    ANOTHER_USER_ORDER_UPDATE_ATTEMPT = 11
    ANOTHER_USER_ORDER_DELETE_ATTEMPT = 12
    AD_ORDER_DOES_NOT_EXIST = 13
    DUPLICATED_PLACEMENT = 14
    ATTEMPT_TO_REMOVE_FOREIGN_PLACEMENT = 15
    PLACEMENT_DOES_NOT_EXIST = 16
    QUERY_PARAMS_VALIDATION_ERROR = 17
    QUERY_PARAMS_INVALID_FORMAT = 18
    ATTEMPT_TO_GET_FOREIGN_CLICKS_DATA = 19


_config = ConfigParser()
_config.read('messages.ini')
ERROR_MESSAGES = _config['errors']


OLDEST_DATE = datetime(1970, 1, 1)


INVALID_ID = 0


class UserTypes:
    AD_PROVIDER = 'ad-provider'
    AD_PLACER = 'ad-placer'

    @classmethod
    def as_choices(cls):
        return [cls.AD_PROVIDER, cls.AD_PLACER]


class AdvertOrderRanks:
    LOW = 1
    MIDDLE = 2
    HIGH = 3

    @classmethod
    def as_choices(cls):
        return [cls.LOW, cls.MIDDLE, cls.HIGH]
