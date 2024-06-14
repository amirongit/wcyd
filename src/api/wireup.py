from typing import Type
from blacksheep import Application, Request, Response, not_found
from redis.asyncio import Redis

from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.abc.service.inode_service import INodeService
from src.infra.node_client import NodeClient
from src.infra.node_repo import NodeRepo
from src.service.node_service import NodeService
from src.settings import NodeSettings, read_settings
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound


SETTINGS = read_settings()


async def inject_dependencies(app: Application) -> None:
    app.services.add_instance(Redis.from_url(str(SETTINGS.REDIS.DSN), decode_responses=True)) # type: ignore
    app.services.add_singleton(INodeRepo, NodeRepo) # type: ignore

    app.services.add_scoped(INodeClient, NodeClient) # type: ignore

    app.services.add_instance(SETTINGS.LOCAL_NODE, NodeSettings) # type: ignore
    app.services.add_singleton(INodeService, NodeService) # type: ignore


async def register_controllers(app: Application) -> None:
    from src.api.controller.node_controller import NodeController


async def register_exception_handlers(app: Application) -> None:

    async def handle_already_connected(
        self,
        request: Request,
        exc: AlreadyExists | Type[AlreadyExists]
    ) -> Response:
        return Response(status=409)

    app.exceptions_handlers[AlreadyExists] = handle_already_connected

    async def handle_already_answered(
        self,
        request: Request,
        exc: AlreadyAnswered | Type[AlreadyAnswered]
    ) -> Response:
        return Response(status=409)

    app.exceptions_handlers[AlreadyAnswered] = handle_already_connected

    async def handle_not_found(
        self,
        request: Request,
        exc: NotFound | Type[NotFound]
    ) -> Response:
        return not_found()

    app.exceptions_handlers[NotFound] = handle_already_connected
