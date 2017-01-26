from aiohttp.web import Request, Response
from extensions.http import HTTPCreated, HTTPBadRequest
from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json
from constants import ApiErrorCodes
from controllers.analytics import AnalyticsController
from validators.analytics import RegisterValidator
from exceptions.analytics import PlacementDoesNotExist


@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_click(request: Request, controller: AnalyticsController, body: dict) -> Response:
    try:
        await controller.register_click(placement_id=body['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_view(request: Request, controller: AnalyticsController, body: dict) -> Response:
    try:
        await controller.register_view(placement_id=body['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)
