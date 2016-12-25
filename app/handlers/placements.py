from aiohttp.web import Request, Response
from extensions.decorators import ad_placer_only, validate_body_json, parse_query_params
from extensions.controllers import bind_controller
from extensions.http import HTTPSuccess, HTTPBadRequest, HTTPNotFound, HTTPCreated, HTTPNoContent, HTTPForbidden
from constants import ApiErrorCodes
from controllers.placements import PlacementsController
from exceptions.placements import (
    DuplicatedPlacement, AdvertOrderDoesNotExist, PlacementDoesNotExist, AttemptToRemoveForeignPlacement
)
from validators.placements import RegisterPlacementValidator
from validators.analytics import YearValidator, MonthValidator, DayValidator


@ad_placer_only
@bind_controller(PlacementsController)
async def get_placements(request: Request, controller: PlacementsController) -> Response:
    data = await controller.get_placements(user=request.user)
    return HTTPSuccess(data=data)


@ad_placer_only
@validate_body_json(RegisterPlacementValidator)
@bind_controller(PlacementsController)
async def create_placement(request: Request, controller: PlacementsController, body: dict) -> Response:
    try:
        data = await controller.create_placement(user=request.user, **body)
        return HTTPCreated(data=data)
    except DuplicatedPlacement as e:
        return HTTPBadRequest(errors={'order_id': e.message}, code=ApiErrorCodes.DUPLICATED_PLACEMENT)
    except AdvertOrderDoesNotExist as e:
        return HTTPBadRequest(errors={'order_id': e.message}, code=ApiErrorCodes.AD_ORDER_DOES_NOT_EXIST)


@ad_placer_only
@bind_controller(PlacementsController)
async def delete_placement(request: Request, controller: PlacementsController) -> Response:
    try:
        await controller.delete_placement(user=request.user, placement_id=request.match_info['placement_id'])
        return HTTPNoContent()
    except PlacementDoesNotExist as e:
        return HTTPNotFound(data={'placement_id': e.message})
    except AttemptToRemoveForeignPlacement as e:
        return HTTPForbidden(errors={'placement_id': e.message},
                             code=ApiErrorCodes.ATTEMPT_TO_REMOVE_FOREIGN_PLACEMENT)


@ad_placer_only
@parse_query_params(YearValidator)
@bind_controller(PlacementsController)
async def get_year_placement_views(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_year_views(request.user,
                                               request.match_info['placement_id'],
                                               params.get('year'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignViews as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_VIEWS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(MonthValidator)
@bind_controller(PlacementsController)
async def get_month_placement_views(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_month_views(request.user,
                                                request.match_info['placement_id'],
                                                params.get('year'),
                                                params.get('month'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignViews as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_VIEWS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(DayValidator)
@bind_controller(PlacementsController)
async def get_day_placement_views(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_day_views(request.user,
                                              request.match_info['placement_id'],
                                              params.get('year'),
                                              params.get('month'),
                                              params.get('day'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignClicks as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_VIEWS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(YearValidator)
@bind_controller(PlacementsController)
async def get_year_placement_clicks(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_year_clicks(request.user,
                                                request.match_info['placement_id'],
                                                params.get('year'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignClicks as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_CLICKS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(MonthValidator)
@bind_controller(PlacementsController)
async def get_month_placement_clicks(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_month_clicks(request.user,
                                                 request.match_info['placement_id'],
                                                 params.get('year'),
                                                 params.get('month'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignClicks as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_CLICKS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)


@ad_placer_only
@parse_query_params(DayValidator)
@bind_controller(PlacementsController)
async def get_day_placement_clicks(request: Request, controller: PlacementsController, params: dict) -> Response:
    try:
        data = await controller.get_day_clicks(request.user,
                                               request.match_info['placement_id'],
                                               params.get('year'),
                                               params.get('month'),
                                               params.get('day'))
        return HTTPSuccess(data=data)
    except AttemptToGetForeignClicks as e:
        return HTTPForbidden(errors={'placement_id': e.message}, code=ApiErrorCodes.ATTEMPT_TO_GET_FOREIGN_CLICKS_DATA)
    except PlacementDoesNotExist as e:
        return HTTPBadRequest(errors={'placement_id': e.message}, code=ApiErrorCodes.PLACEMENT_DOES_NOT_EXIST)
