from aiohttp.web import Application, Response


class ImproperlyConfigured(Exception):
    pass


class App(Application):

    def __init__(self, *, db, route_config, **kwargs):
        super().__init__(**kwargs)
        self.__db = db
        self.configure_routes(route_config)

    def make_options_handler(self, methods):
        async def options_handler(request):
            response = Response()
            ms = list(methods)
            ms.append('OPTIONS')
            response.headers['Access-Control-Allow-Methods'] = ', '.join([m.upper() for m in ms])
            return response
        return options_handler

    @property
    def db(self):
        return self.__db

    def configure_routes(self, route_config: dict):
        for path, config in route_config.items():
            if 'name' not in config:
                raise ImproperlyConfigured('Resource should have name')
            if 'methods' not in config:
                raise ImproperlyConfigured('Resource should have allowed methods')
            if not len(config['methods']):
                raise ImproperlyConfigured('Resource should have at least one allowed method')

            resource = self.router.add_resource(path, name=config['name'])

            for method, handler in config['methods'].items():
                resource.add_route(method, handler)
            resource.add_route('options', self.make_options_handler(config['methods'].keys()))

    def get_url(self, resource_name, parts=None, query=None):
        kwargs = {}
        if parts is not None:
            kwargs['parts'] = parts
        return self.router[resource_name].url(query=query, **kwargs)
