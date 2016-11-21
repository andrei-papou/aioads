from aiohttp.web import Request, Response
from extensions.decorators import ad_placer_only, validate_body_json
from extensions.controllers import bind_controller
from extensions.http import HTTPSuccess, HTTPBadRequest, HTTPNotFound, HTTPCreated
from constants import ApiErrorCodes
from controllers.placements import PlacementsController
from exceptions.placements import DuplicatedPlacement, AdvertOrderDoesNotExist
from validators.placements import RegisterPlacementValidator


@ad_placer_only
@bind_controller(PlacementsController)
async def get_placements(request: Request, controller: PlacementsController) -> Response:
    data = await controller.get_placements(user=request.user)
    return HTTPSuccess(data=data)


@ad_placer_only
@validate_body_json(RegisterPlacementValidator)
@bind_controller(PlacementsController)
async def create_placement(request: Request, controller: PlacementsController) -> Response:
    try:
        data = await controller.create_placement(user=request.user, **request.data)
        return HTTPCreated(data=data)
    except DuplicatedPlacement as e:
        return HTTPBadRequest(errors={'order_id': e.message}, code=ApiErrorCodes.DUPLICATED_PLACEMENT)
    except AdvertOrderDoesNotExist as e:
        return HTTPBadRequest(errors={'order_id': e.message}, code=ApiErrorCodes.AD_ORDER_DOES_NOT_EXIST)
