from configparser import ConfigParser


class ApiErrorCodes:
    BODY_VALIDATION_ERROR = 1
    INVALID_BODY_JSON = 2
    EMAIL_ALREADY_IN_USE = 3
    WEBSITE_IS_ALREADY_REGISTERED = 4
    USER_DOES_NOT_EXIST = 5
    PASSWORD_IS_INVALID = 6


_config = ConfigParser()
_config.read('messages.ini')
ERROR_MESSAGES = _config['errors']
