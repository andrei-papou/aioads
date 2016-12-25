from extensions.http import GET, POST, DELETE, PATCH
from handlers.auth import signup_ad_placer, signup_ad_provider, login, get_user_data
from handlers.advert_orders import (
    get_advert_orders, get_advert_order, create_advert_order, update_advert_order, delete_advert_order,
    get_year_advert_order_views, get_year_advert_order_clicks, get_month_advert_order_views,
    get_month_advert_order_clicks, get_day_advert_order_views, get_day_advert_order_clicks
)
from handlers.placements import (
    get_placements, create_placement, delete_placement, get_year_placement_clicks,
    get_year_placement_views, get_month_placement_views, get_day_placement_views,
    get_month_placement_clicks, get_day_placement_clicks,
)
from handlers.analytics import register_click, register_view


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

    AD_ORDER_YEAR_CLICKS = 'ad-order-year-clicks'
    AD_ORDER_MONTH_CLICKS = 'ad-order-month-clicks'
    AD_ORDER_DAY_CLICKS = 'ad-order-day-clicks'

    AD_ORDER_YEAR_VIEWS = 'ad-order-year-views'
    AD_ORDER_MONTH_VIEWS = 'ad-order-month-views'
    AD_ORDER_DAY_VIEWS = 'ad-order-day-views'

    PLACEMENT_YEAR_CLICKS = 'placement-year-clicks'
    PLACEMENT_MONTH_CLICKS = 'placement-month-clicks'
    PLACEMENT_DAY_CLICKS = 'placement-day-clicks'

    PLACEMENT_YEAR_VIEWS = 'placement-year-views'
    PLACEMENT_MONTH_VIEWS = 'placement-month-views'
    PLACEMENT_DAY_VIEWS = 'placement-day-views'


route_config = {
    '/signup-ad-placer': {
        'name': EndpointsMapper.AD_PLACER_SIGNUP,
        'methods': {POST: signup_ad_placer}
    },
    '/signup-ad-provider': {
        'name': EndpointsMapper.AD_PROVIDER_SIGNUP,
        'methods': {POST: signup_ad_provider}
    },
    '/login': {
        'name': EndpointsMapper.LOGIN,
        'methods': {POST: login}
    },
    '/account-data': {
        'name': EndpointsMapper.USER_DATA,
        'methods': {GET: get_user_data}
    },
    '/advert-orders': {
        'name': EndpointsMapper.ADVERT_ORDERS,
        'methods': {
            GET: get_advert_orders,
            POST: create_advert_order
        }
    },
    '/advert-orders/{order_id}': {
        'name': EndpointsMapper.ADVERT_ORDER,
        'methods': {
            GET: get_advert_order,
            PATCH: update_advert_order,
            DELETE: delete_advert_order
        }
    },
    '/advert-orders/{order_id}/year-views': {
        'name': EndpointsMapper.AD_ORDER_YEAR_VIEWS,
        'methods': {GET: get_year_advert_order_views}
    },
    '/advert-orders/{order_id}/month-views': {
        'name': EndpointsMapper.AD_ORDER_MONTH_VIEWS,
        'methods': {GET: get_month_advert_order_views}
    },
    '/advert-orders/{order_id}/day-views': {
        'name': EndpointsMapper.AD_ORDER_DAY_VIEWS,
        'methods': {GET: get_day_advert_order_views}
    },
    '/advert-orders/{order_id}/year-clicks': {
        'name': EndpointsMapper.AD_ORDER_YEAR_CLICKS,
        'methods': {GET: get_year_advert_order_clicks}
    },
    '/advert-orders/{order_id}/month-clicks': {
        'name': EndpointsMapper.AD_ORDER_MONTH_CLICKS,
        'methods': {GET: get_month_advert_order_clicks}
    },
    '/advert-orders/{order_id}/day-clicks': {
        'name': EndpointsMapper.AD_ORDER_DAY_CLICKS,
        'methods': {GET: get_day_advert_order_clicks}
    },
    '/placements': {
        'name': EndpointsMapper.PLACEMENTS,
        'methods': {
            GET: get_placements,
            POST: create_placement
        }
    },
    '/placements/{placement_id}': {
        'name': EndpointsMapper.PLACEMENT,
        'methods': {DELETE: delete_placement}
    },
    '/placements/{placement_id}/year-clicks': {
        'name': EndpointsMapper.PLACEMENT_YEAR_CLICKS,
        'methods': {GET: get_year_placement_clicks}
    },
    '/placements/{placement_id}/month-clicks': {
        'name': EndpointsMapper.PLACEMENT_MONTH_CLICKS,
        'methods': {GET: get_month_placement_clicks}
    },
    '/placements/{placement_id}/day-clicks': {
        'name': EndpointsMapper.PLACEMENT_DAY_CLICKS,
        'methods': {GET: get_day_placement_clicks}
    },
    '/placements/{placement_id}/year-views': {
        'name': EndpointsMapper.PLACEMENT_YEAR_VIEWS,
        'methods': {GET: get_year_placement_views}
    },
    '/placements/{placement_id}/month-views': {
        'name': EndpointsMapper.PLACEMENT_MONTH_VIEWS,
        'methods': {GET: get_month_placement_views}
    },
    '/placements/{placement_id}/day-views': {
        'name': EndpointsMapper.PLACEMENT_DAY_VIEWS,
        'methods': {GET: get_day_placement_views}
    },
    '/analytics/clicks': {
        'name': EndpointsMapper.CLICKS,
        'methods': {POST: register_click}
    },
    '/analytics/views': {
        'name': EndpointsMapper.VIEWS,
        'methods': {POST: register_view}
    }
}
