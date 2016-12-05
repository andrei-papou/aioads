from extensions.http import HTTPMethods
from handlers.auth import signup_ad_placer, signup_ad_provider, login, get_user_data
from handlers.advert_orders import get_advert_orders, create_advert_order, update_advert_order, delete_advert_order
from handlers.placements import get_placements, create_placement, delete_placement
from handlers.analytics import register_click


class EndpointsMapper:
    AD_PLACER_SIGNUP = 'ad-placer-signup'
    AD_PROVIDER_SIGNUP = 'ad-provider-signup'
    LOGIN = 'login'
    USER_DATA = 'user-data'

    ADVERT_ORDERS = 'advert-orders'
    ADVERT_ORDER = 'advert-order'

    PLACEMENTS = 'placements'
    PLACEMENT = 'placement'

    CLICKS = 'clicks'


route_config = {
    '/signup-ad-placer': {
        'name': EndpointsMapper.AD_PLACER_SIGNUP,
        'methods': {
            HTTPMethods.POST: signup_ad_placer
        }
    },
    '/signup-ad-provider': {
        'name': EndpointsMapper.AD_PROVIDER_SIGNUP,
        'methods': {
            HTTPMethods.POST: signup_ad_provider
        }
    },
    '/login': {
        'name': EndpointsMapper.LOGIN,
        'methods': {
            HTTPMethods.POST: login
        }
    },
    '/account-data': {
        'name': EndpointsMapper.USER_DATA,
        'methods': {
            HTTPMethods.GET: get_user_data
        }
    },
    '/advert-orders': {
        'name': EndpointsMapper.ADVERT_ORDERS,
        'methods': {
            HTTPMethods.GET: get_advert_orders,
            HTTPMethods.POST: create_advert_order
        }
    },
    '/advert-orders/{order_id}': {
        'name': EndpointsMapper.ADVERT_ORDER,
        'methods': {
            HTTPMethods.PATCH: update_advert_order,
            HTTPMethods.DELETE: delete_advert_order
        }
    },
    '/placements': {
        'name': EndpointsMapper.PLACEMENTS,
        'methods': {
            HTTPMethods.GET: get_placements,
            HTTPMethods.POST: create_placement
        }
    },
    '/placements/{placement_id}': {
        'name': EndpointsMapper.PLACEMENT,
        'methods': {
            HTTPMethods.DELETE: delete_placement
        }
    },
    '/analytics/clicks': {
        'name': EndpointsMapper.CLICKS,
        'methods': {
            HTTPMethods.POST: register_click
        }
    }
}
