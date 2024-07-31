from blacksheep import Application

from src.api.wireup import (
    inject_dependencies,
    register_controllers,
    register_exception_handlers,
    register_authentication_handlers
)
from src.api.docs import docs


app = Application(show_error_details=True)

app.on_start(inject_dependencies)
app.on_start(register_controllers)
app.on_start(register_exception_handlers)
app.on_start(register_authentication_handlers)

docs.bind_app(app)


if __name__ == '__main__':
    from uvicorn import run
    run('src.api.entrypoint:app', host='0.0.0.0', port=44777, log_level='debug', lifespan='on', reload=True)
