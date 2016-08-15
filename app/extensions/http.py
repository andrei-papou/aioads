import json
from aiohttp.web import Response


class StatusCodes:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
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


class HTTPSuccess(JSONBodyResponse):
    status_code = StatusCodes.OK


class HTTPCreated(JSONBodyResponse):
    status_code = StatusCodes.CREATED


class HTTPNoContent(JSONBodyResponse):
    status_code = StatusCodes.NO_CONTENT


class HTTPBadRequest(JSONBodyResponse):
    status_code = StatusCodes.BAD_REQUEST

    def __init__(self, *args, errors={}, **kwargs):
        kwargs['data'] = {'errors': errors}
        super().__init__(*args, **kwargs)


class HTTPUnauthorized(JSONBodyResponse):
    status_code = StatusCodes.UNAUTHORIZED


class HTTPForbidden(JSONBodyResponse):
    status_code = StatusCodes.FORBIDDEN


class HTTPMethodNotAllowed(JSONBodyResponse):
    status_code = StatusCodes.METHOD_NOT_ALLOWED
