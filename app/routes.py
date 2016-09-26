from extensions.http import HTTPMethods
from handlers.auth import signup_ad_placer, signup_ad_provider, login, get_user_data
from handlers.advert_orders import get_advert_orders


class EndpointsMapper:
    AD_PLACER_SIGNUP = '/signup-ad-placer'
    AD_PROVIDER_SIGNUP = '/signup-ad-provider'
    LOGIN = '/login'
    USER_DATA = '/account-data'

    ADVERT_ORDERS = '/advert-orders'


routes = (
    (HTTPMethods.POST, EndpointsMapper.AD_PLACER_SIGNUP, signup_ad_placer),
    (HTTPMethods.POST, EndpointsMapper.AD_PROVIDER_SIGNUP, signup_ad_provider),
    (HTTPMethods.POST, EndpointsMapper.LOGIN, login),
    (HTTPMethods.GET, EndpointsMapper.USER_DATA, get_user_data),

    (HTTPMethods.GET, EndpointsMapper.ADVERT_ORDERS, get_advert_orders),
)
