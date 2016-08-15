from extensions.controllers import bind_controller
from extensions.decorators import validate_body_json
from extensions.http import HTTPCreated, HTTPBadRequest, HTTPSuccess
from controllers.auth import AuthController
from validators.auth import AdPlacerSignupValidator, AdProviderSignupValidator, LoginValidator
from exceptions.auth import EmailAlreadyInUse, WebsiteAlreadyRegistered, UserDoesNotExist, InvalidPassword


@validate_body_json(AdPlacerSignupValidator)
@bind_controller(AuthController)
async def signup_ad_placer(request, controller):
    try:
        token = await controller.signup_ad_placer(**request.data)
        return HTTPCreated(data={'token': token})
    except EmailAlreadyInUse as e:
        return HTTPBadRequest(errors={'email': [e.message]})
    except WebsiteAlreadyRegistered as e:
        return HTTPBadRequest(errors={'website': [e.message]})


@validate_body_json(AdProviderSignupValidator)
@bind_controller(AuthController)
async def signup_ad_provider(request, controller):
    try:
        token = await controller.signup_ad_provider(**request.data)
        return HTTPCreated(data={'token': token})
    except EmailAlreadyInUse as e:
        return HTTPBadRequest(errors={'email': [e.message]})


@validate_body_json(LoginValidator)
@bind_controller(AuthController)
async def login(request, controller):
    try:
        token = await controller.login(**request.data)
        return HTTPSuccess(data={'token': token})
    except UserDoesNotExist as e:
        return HTTPBadRequest(errors={'email': [e.message]})
    except InvalidPassword as e:
        return HTTPBadRequest(errors={'password': [e.message]})
