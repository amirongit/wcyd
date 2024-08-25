from blacksheep import Application
from guardpost import Policy
from guardpost.common import AuthenticatedRequirement

from src.api.auth import DecentralizedAuthenticationHandler
from src.api.docs import docs
from src.api.wireup import (
    inject_dependencies,
    register_controllers,
    register_exception_handlers,
)

app = Application(show_error_details=False)

app.on_start(inject_dependencies)
app.on_start(register_controllers)
app.on_start(register_exception_handlers)

app.use_authentication().add(DecentralizedAuthenticationHandler(app))
app.use_authorization().default_policy = Policy('authenticated', AuthenticatedRequirement())
docs.bind_app(app)


if __name__ == '__main__':
    from uvicorn import run
    run('src.api.entrypoint:app', host='0.0.0.0', port=44777, log_level='debug', lifespan='on', reload=True)
