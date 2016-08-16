from extensions.http import HTTPMethods
from handlers.auth import signup_ad_placer, signup_ad_provider, login


class EndpointsMapper:
    AD_PLACER_SIGNUP = '/signup-ad-placer'
    AD_PROVIDER_SIGNUP = '/signup-ad-provider'
    LOGIN = '/login'


routes = (
    ( HTTPMethods.POST, EndpointsMapper.AD_PLACER_SIGNUP, signup_ad_placer ),
    ( HTTPMethods.POST, EndpointsMapper.AD_PROVIDER_SIGNUP, signup_ad_provider ),
    ( HTTPMethods.POST, EndpointsMapper.LOGIN, login ),
)
