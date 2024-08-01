from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info, Response, Operation, OpenAPI, HTTPSecurity, Security, SecurityRequirement


def unsecure_handler(self: OpenAPIHandler, operation: Operation) -> None:
    operation.security = list()


class SecuredOpenAPIHandler(OpenAPIHandler):
    def on_docs_generated(self, docs: OpenAPI) -> None:
        docs.components.security_schemes = {'Basic authentication': HTTPSecurity(scheme='Basic')} # type: ignore
        docs.security = Security(requirements=[SecurityRequirement(name='Basic authentication', value=list())])
        super().on_docs_generated(docs)

docs = SecuredOpenAPIHandler(info=Info(title='WCYD', version='0'))
docs.common_responses = {
    400: Response('bad request'),
    401: Response('unauthenticated'),
    500: Response('internal error')
}
