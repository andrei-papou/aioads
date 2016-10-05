import json
from aiohttp.web import Response
from constants import ERROR_MESSAGES


class StatusCodes:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405


class HTTPMethods:
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    PATCH = 'patch'
    DELETE = 'delete'


class StatusCodeResponse(Response):
    status_code = None

    def __init__(self, **kwargs):
        if self.status_code is None:
            raise NotImplementedError('Unknown status code')
        kwargs['status'] = self.status_code
        super(StatusCodeResponse, self).__init__(**kwargs)


class JSONBodyResponse(StatusCodeResponse):
    CONTENT_TYPE = 'application/json'

    def __init__(self, *args, data={}, **kwargs):
        kwargs['content_type'] = self.CONTENT_TYPE
        kwargs['text'] = json.dumps(data)
        super(JSONBodyResponse, self).__init__(**kwargs)


class ApiErrorCodeResponse(JSONBodyResponse):

    def __init__(self, code, *args, errors=None, **kwargs):
        errors = errors or {}
        kwargs['data'] = {
            'code': code,
            'message': ERROR_MESSAGES[str(code)],
            'errors': errors
        }
        super().__init__(*args, **kwargs)


class HTTPSuccess(JSONBodyResponse):
    status_code = StatusCodes.OK


class HTTPCreated(JSONBodyResponse):
    status_code = StatusCodes.CREATED


class HTTPNoContent(JSONBodyResponse):
    status_code = StatusCodes.NO_CONTENT


class HTTPBadRequest(ApiErrorCodeResponse):
    status_code = StatusCodes.BAD_REQUEST


class HTTPUnauthorized(JSONBodyResponse):
    status_code = StatusCodes.UNAUTHORIZED


class HTTPForbidden(ApiErrorCodeResponse):
    status_code = StatusCodes.FORBIDDEN


class HTTPNotFound(JSONBodyResponse):
    status_code = StatusCodes.NOT_FOUND


class HTTPMethodNotAllowed(JSONBodyResponse):
    status_code = StatusCodes.METHOD_NOT_ALLOWED
