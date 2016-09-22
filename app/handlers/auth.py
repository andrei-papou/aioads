from aiohttp.web import Request, Response
from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json, auth_required
from extensions.http import HTTPCreated, HTTPBadRequest, HTTPSuccess
from controllers.auth import AuthController
from validators.auth import AdPlacerSignupValidator, AdProviderSignupValidator, LoginValidator
from exceptions.auth import EmailAlreadyInUse, WebsiteAlreadyRegistered, UserDoesNotExist, InvalidPassword
from constants import ApiErrorCodes


@validate_body_json(AdPlacerSignupValidator)
@bind_controller(AuthController)
async def signup_ad_placer(request: Request, controller: AuthController) -> Response:
    try:
        token = await controller.signup_ad_placer(**request.data)
        return HTTPCreated(data={'token': token})
    except EmailAlreadyInUse as e:
        return HTTPBadRequest(errors={'email': [e.message]}, code=ApiErrorCodes.EMAIL_ALREADY_IN_USE)
    except WebsiteAlreadyRegistered as e:
        return HTTPBadRequest(errors={'website': [e.message]}, code=ApiErrorCodes.WEBSITE_IS_ALREADY_REGISTERED)


@validate_body_json(AdProviderSignupValidator)
@bind_controller(AuthController)
async def signup_ad_provider(request: Request, controller: AuthController) -> Response:
    try:
        token = await controller.signup_ad_provider(**request.data)
        return HTTPCreated(data={'token': token})
    except EmailAlreadyInUse as e:
        return HTTPBadRequest(errors={'email': [e.message]}, code=ApiErrorCodes.EMAIL_ALREADY_IN_USE)


@validate_body_json(LoginValidator)
@bind_controller(AuthController)
async def login(request: Request, controller: AuthController) -> Response:
    try:
        token = await controller.login(**request.data)
        return HTTPSuccess(data={'token': token})
    except UserDoesNotExist as e:
        return HTTPBadRequest(errors={'email': [e.message]}, code=ApiErrorCodes.USER_DOES_NOT_EXIST)
    except InvalidPassword as e:
        return HTTPBadRequest(errors={'password': [e.message]}, code=ApiErrorCodes.PASSWORD_IS_INVALID)


@auth_required
async def get_user_data(request: Request):
    return HTTPSuccess(data=request.user.as_dict())
