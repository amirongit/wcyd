from blacksheep import Application

from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.abc.service.inode_service import INodeService
from src.infra.node_client import NodeClient
from src.infra.node_repo import NodeRepo
from src.service.node_service import NodeService
from src.settings import Settings, SETTINGS


async def inject_dependencies(app: Application) -> None:
    app.services.add_instance(SETTINGS) # type: ignore
    app.services.add_instance(INodeService, NodeService) # type: ignore
    app.services.add_instance(INodeRepo, NodeRepo) # type: ignore
    app.services.add_instance(INodeClient, NodeClient) # type: ignore


async def register_controllers(app: Application) -> None:
    from src.api.controller.node_controller import NodeController
