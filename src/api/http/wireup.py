from blacksheep import Application

from src.core.local_node import LocalNode
from src.settings import SETTINGS


async def inject_dependencies(app: Application) -> None:
    app.services.add_instance( # type: ignore
        LocalNode(
            SETTINGS.LOCAL_NODE.IDENTIFIER,
            SETTINGS.LOCAL_NODE.PUBLIC_KEY,
            str(SETTINGS.LOCAL_NODE.ENDPOINT),
        )
    )


async def register_controllers(app: Application) -> None:
    from src.api.http.controller.node_controller import NodeController
