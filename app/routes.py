from extensions.http import HTTPMethods
from handlers.auth import signup_ad_placer, signup_ad_provider, login, get_user_data
from handlers.advert_orders import get_advert_orders, create_advert_order, update_advert_order, delete_advert_order
from handlers.placements import get_placements, create_placement, delete_placement
from handlers.analytics import register_click, register_view, get_year_placement_clicks, get_month_placement_clicks


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
    VIEWS = 'views'

    PLACEMENT_YEAR_CLICKS = 'placement-year-clicks'
    PLACEMENT_MONTH_CLICKS = 'placement-month-clicks'


route_config = {
    '/signup-ad-placer': {
        'name': EndpointsMapper.AD_PLACER_SIGNUP,
        'methods': {HTTPMethods.POST: signup_ad_placer}
    },
    '/signup-ad-provider': {
        'name': EndpointsMapper.AD_PROVIDER_SIGNUP,
        'methods': {HTTPMethods.POST: signup_ad_provider}
    },
    '/login': {
        'name': EndpointsMapper.LOGIN,
        'methods': {HTTPMethods.POST: login}
    },
    '/account-data': {
        'name': EndpointsMapper.USER_DATA,
        'methods': {HTTPMethods.GET: get_user_data}
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
        'methods': {HTTPMethods.DELETE: delete_placement}
    },
    '/analytics/clicks': {
        'name': EndpointsMapper.CLICKS,
        'methods': {HTTPMethods.POST: register_click}
    },
    '/analytics/placement/{placement_id}/year-clicks': {
        'name': EndpointsMapper.PLACEMENT_YEAR_CLICKS,
        'methods': {HTTPMethods.GET: get_year_placement_clicks}
    },
    '/analytics/placement/{placement_id}/month-clicks': {
        'name': EndpointsMapper.PLACEMENT_MONTH_CLICKS,
        'methods': {HTTPMethods.GET: get_month_placement_clicks}
    },
    '/analytics/views': {
        'name': EndpointsMapper.VIEWS,
        'methods': {HTTPMethods.POST: register_view}
    }
}
