import logging


class BaseSettings:
    JWT_HEADER = 'Authorization'
    JWT_SECRET = '@#FUH#(*YF&Y#M+*#YU#*RY+ce*Y#xU*lJE(kyt#U=-)@afe!v'
    JWT_ALGORITHM = 'HS256'
    JWT_EXT_DELTA_SECODNS = 365 * 24 * 3600

    THREAD_POOL_LIMIT = 2

    LOGGER_NAME = 'ads-logger'


class DevSettings(BaseSettings):
    HOST = '0.0.0.0'
    PORT = 8000

    DB_USER = 'admin'
    DB_NAME = 'ads-dev'
    DB_HOST = '127.0.0.1'
    DB_PASS = 'homm1994'

    TEST_DB_USER = 'qabot'
    TEST_DB_NAME = 'ads-dev-test'
    TEST_DB_HOST = '127.0.0.1'
    TEST_DB_PASS = 'homm1994'

    SALT_ROUNDS = 10

    LOGGER_LEVEL = logging.DEBUG


settings = DevSettings
