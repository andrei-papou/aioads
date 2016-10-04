from aiohttp.web import Request, Response
from extensions.http import HTTPSuccess, HTTPCreated, HTTPBadRequest
from extensions.controllers import bind_controller
from extensions.decorators import auth_required, validate_body_json, ad_provider_only
from controllers.advert_orders import AdvertOrdersController
from exceptions.advert_orders import AdvertOrderForSuchLinkAlreadyExists
from validators.advert_orders import CreateAdvertValidator
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
