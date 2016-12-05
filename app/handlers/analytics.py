from aiohttp.web import Request, Response
from extensions.http import HTTPCreated
from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json, ad_placer_only
from controllers.analytics import AnalyticsController
from validators.analytics import RegisterClickValidator


@ad_placer_only
@validate_body_json(RegisterClickValidator)
@bind_controller(AnalyticsController)
async def register_click(request: Request, controller: AnalyticsController) -> Response:
    await controller.register_click(placement_id=request.data['placement_id'])
    return HTTPCreated()
