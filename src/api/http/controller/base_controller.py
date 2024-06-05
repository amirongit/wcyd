from blacksheep.server.controllers import APIController


class BaseController(APIController):

    ROUTE: str = ''
    VERSION: int = 1

    @classmethod
    def version(cls) -> str:
        return str(cls.VERSION)

    @classmethod
    def route(cls) -> str:
        return f'api/{cls.version()}/{cls.ROUTE}'
