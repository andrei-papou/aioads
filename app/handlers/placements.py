from aiohttp.web import Request, Response
from extensions.decorators import ad_placer_only
from extensions.controllers import bind_controller
from extensions.http import HTTPSuccess
from controllers.placements import PlacementsController


@ad_placer_only
@bind_controller(PlacementsController)
async def get_placements(request: Request, controller: PlacementsController) -> Response:
    data = await controller.get_placements(user=request.user)
    return HTTPSuccess(data=data)
