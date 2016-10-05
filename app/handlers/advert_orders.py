from aiohttp.web import Request, Response
from extensions.http import HTTPSuccess, HTTPCreated, HTTPBadRequest, HTTPForbidden, HTTPNotFound
from extensions.controllers import bind_controller
from extensions.decorators import auth_required, validate_body_json, ad_provider_only
from controllers.advert_orders import AdvertOrdersController
from exceptions.advert_orders import (
    AdvertOrderForSuchLinkAlreadyExists, AdvertOrderDoesNotExist, AnotherUserOrderUpdateAttempt
)
from validators.advert_orders import CreateAdvertValidator, UpdateAdvertValidator
from constants import ApiErrorCodes


@auth_required
@bind_controller(AdvertOrdersController)
async def get_advert_orders(request: Request, controller: AdvertOrdersController) -> Response:
    result = await controller.get_orders()
    return HTTPSuccess(data=result)


@ad_provider_only
@validate_body_json(CreateAdvertValidator)
@bind_controller(AdvertOrdersController)
async def create_advert_order(request: Request, controller: AdvertOrdersController) -> Response:
    try:
        response_data = await controller.create_order(**request.data, user=request.user)
        return HTTPCreated(data=response_data)
    except AdvertOrderForSuchLinkAlreadyExists as e:
        return HTTPBadRequest(errors={'follow_url_link': e.message}, code=ApiErrorCodes.AD_ORDER_FOR_LINK_EXISTS)


@ad_provider_only
@validate_body_json(UpdateAdvertValidator)
@bind_controller(AdvertOrdersController)
async def update_advert_order(request: Request, controller: AdvertOrdersController) -> Response:
    try:
        response_data = await controller.update_order(request.match_info['order_id'], request.user, **request.data)
        return HTTPSuccess(data=response_data)
    except AnotherUserOrderUpdateAttempt as e:
        return HTTPForbidden(code=ApiErrorCodes.ANOTHER_USER_ORDER_UPDATE_ATTEMPT,
                             errors={'order_id': e.message})
    except AdvertOrderDoesNotExist as e:
        return HTTPNotFound(data={'order_id': e.message})
