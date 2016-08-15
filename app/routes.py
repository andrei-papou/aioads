from extensions.http import HTTPMethods
from handlers.auth import signup_ad_placer, signup_ad_provider, login


class URLMapper:
    AD_PLACER_SIGNUP = '/signup-ad-placer'
    AD_PROVIDER_SIGNUP = '/signup-ad-provider'
    LOGIN = '/login'


routes = (
    ( HTTPMethods.POST, URLMapper.AD_PLACER_SIGNUP, signup_ad_placer ),
    ( HTTPMethods.POST, URLMapper.AD_PROVIDER_SIGNUP, signup_ad_provider ),
    ( HTTPMethods.POST, URLMapper.LOGIN, login ),
)
