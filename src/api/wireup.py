from typing import Type

from blacksheep import Application, Request, Response, not_found
from redis.asyncio import Redis

from src.settings import read_settings

SETTINGS = read_settings()


async def inject_dependencies(app: Application) -> None:
    from src.abc.infra.imessage_repo import IMessageRepo
    from src.abc.infra.inode_client import INodeClient
    from src.abc.infra.inode_repo import INodeRepo
    from src.abc.infra.ipeer_repo import IPeerRepo
    from src.abc.use_case.add_peer_use_case import AddPeerUseCase
    from src.abc.use_case.connect_node_use_case import ConnectNodeUseCase
    from src.abc.use_case.find_node_use_case import FindNodeUseCase
    from src.abc.use_case.find_peer_use_case import FindPeerUseCase
    from src.abc.use_case.get_related_messages_use_case import GetRelatedMessagesUseCase
    from src.abc.use_case.remove_peer_use_case import RemovePeerUseCase
    from src.abc.use_case.send_message_use_case import SendMessageUseCase
    from src.infra.message_repo import MessageRepo
    from src.infra.node_client import NodeClient
    from src.infra.node_repo import NodeRepo
    from src.infra.peer_repo import PeerRepo
    from src.settings import AuthenticationSettings, NodeSettings
    from src.use_case.add_peer import AddPeer
    from src.use_case.connect_node import ConnectNode
    from src.use_case.find_node import FindNode
    from src.use_case.find_peer import FindPeer
    from src.use_case.get_related_messages import GetRelatedMessages
    from src.use_case.remove_peer import RemovePeer
    from src.use_case.send_message import SendMessage

    app.services.add_instance(Redis.from_url(str(SETTINGS.REDIS.DSN), decode_responses=True))  # type: ignore
    app.services.add_singleton(INodeRepo, NodeRepo)  # type: ignore
    app.services.add_singleton(IPeerRepo, PeerRepo)  # type: ignore
    app.services.add_singleton(IMessageRepo, MessageRepo)  # type: ignore
    app.services.add_scoped(INodeClient, NodeClient)  # type: ignore
    app.services.add_instance(SETTINGS.LOCAL_NODE, NodeSettings)  # type: ignore
    app.services.add_instance(SETTINGS.AUTHENTICATION, AuthenticationSettings)  # type: ignore
    app.services.add_singleton(AddPeerUseCase, AddPeer)  # type: ignore
    app.services.add_singleton(ConnectNodeUseCase, ConnectNode)  # type: ignore
    app.services.add_singleton(FindNodeUseCase, FindNode)  # type: ignore
    app.services.add_singleton(FindPeerUseCase, FindPeer)  # type: ignore
    app.services.add_singleton(GetRelatedMessagesUseCase, GetRelatedMessages)  # type: ignore
    app.services.add_singleton(RemovePeerUseCase, RemovePeer)  # type: ignore
    app.services.add_singleton(SendMessageUseCase, SendMessage)  # type: ignore


async def register_controllers(app: Application) -> None:
    from src.api.controller.message_controller import MessageController
    from src.api.controller.node_controller import NodeController
    from src.api.controller.peer_controller import PeerController
    from src.api.controller.related_message_controller import RelatedMessageController
    from src.api.controller.related_peer_controller import RelatedPeerController


async def register_exception_handlers(app: Application) -> None:
    from src.type.exception import AlreadyAnswered, AlreadyExists, DoesNotExist

    async def handle_already_exists(
        self: Application, request: Request, exc: AlreadyExists | Type[AlreadyExists]
    ) -> Response:
        return Response(status=409)

    app.exceptions_handlers[AlreadyExists] = handle_already_exists

    async def handle_already_answered(
        self: Application, request: Request, exc: AlreadyAnswered | Type[AlreadyAnswered]
    ) -> Response:
        return Response(status=409)

    app.exceptions_handlers[AlreadyAnswered] = handle_already_answered

    async def handle_not_found(self: Application, request: Request, exc: DoesNotExist | Type[DoesNotExist]) -> Response:
        return not_found()

    app.exceptions_handlers[DoesNotExist] = handle_not_found
