from aiohttp.web import Request, Response
from extensions.http import HTTPSuccess
from extensions.controllers import bind_controller
from extensions.decorators import auth_required
from controllers.advert_orders import AdvertOrdersController


@auth_required
@bind_controller(AdvertOrdersController)
async def get_advert_orders(request: Request, controller: AdvertOrdersController) -> Response:
    result = await controller.get_orders()
    return HTTPSuccess(data=result)
