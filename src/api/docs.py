from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info, Response

docs = OpenAPIHandler(info=Info(title='WCYD', version='0'))
docs.common_responses = {400: Response('bad request'), 500: Response('internal error')}
