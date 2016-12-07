from aiohttp.web import Request, Response
from extensions.http import HTTPCreated, HTTPBadRequest, HTTPSuccess, HTTPForbidden
from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json, ad_placer_only, parse_query_params
from constants import ApiErrorCodes
from controllers.analytics import AnalyticsController
from validators.analytics import RegisterValidator, YearValidator
from exceptions.analytics import PlacementDoesNotExist, AttemptToGetForeignClicks


@ad_placer_only
@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_click(request: Request, controller: AnalyticsController, body: dict) -> Response:
    try:
        await controller.register_click(placement_id=body['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@validate_body_json(RegisterValidator)
@bind_controller(AnalyticsController)
async def register_view(request: Request, controller: AnalyticsController, body: dict) -> Response:
    try:
        await controller.register_view(placement_id=body['placement_id'])
        return HTTPCreated()
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(YearValidator)
@bind_controller(AnalyticsController)
async def get_year_placement_clicks(request: Request, controller: AnalyticsController, params: dict) -> Response:
    try:
        data = await controller.get_year_clicks_for_placement(request.user, request.match_info['placement_id'], params.get('year'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignClicks as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_CLICKS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)
