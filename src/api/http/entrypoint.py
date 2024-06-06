from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from uvicorn import run

from src.api.http.wireup import inject_dependencies, register_controllers


docs = OpenAPIHandler(info=Info(title="WCYD", version="0"))
app = Application(show_error_details=True)

app.on_start(inject_dependencies)
app.on_start(register_controllers)

docs.bind_app(app)


if __name__ == '__main__':
    run('src.api.http.entrypoint:app', host='0.0.0.0', port=44777, log_level='debug', lifespan='on', reload=True)
