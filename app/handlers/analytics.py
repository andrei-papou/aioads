from aiohttp.web import Request, Response
from extensions.http import HTTPCreated, HTTPBadRequest
from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json, ad_placer_only
from constants import ApiErrorCodes
from controllers.analytics import AnalyticsController
from validators.analytics import RegisterValidator
from exceptions.analytics import PlacementDoesNotExist


@ad_placer_only
@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_click(request: Request, controller: AnalyticsController) -> Response:
    try:
        await controller.register_click(placement_id=request.data['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_view(request: Request, controller: AnalyticsController) -> Response:
    try:
        await controller.register_view(placement_id=request.data['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)
