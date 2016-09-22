from aiohttp.web import Application


class App(Application):

    def __init__(self, *, db, **kwargs):
        super().__init__(**kwargs)
        self.__db = db

    @property
    def db(self):
        return self.__db
