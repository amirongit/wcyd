from src.abc.infra.imessage_repo import IMessageRepo
from src.abc.infra.inode_client import INodeClient
from src.abc.infra.ipeer_repo import IPeerRepo
from src.abc.use_case.find_node_use_case import FindNodeUseCase
from src.abc.use_case.send_message_use_case import SendMessageUseCase
from src.settings import NodeSettings
from src.type.exception import DoesNotExist
from src.type.internal import UniversalPeerIdentifier


class SendMessage(SendMessageUseCase):
    def __init__(
        self,
        find_node_use_case: FindNodeUseCase,
        node_client: INodeClient,
        message_repo: IMessageRepo,
        peer_repo: IPeerRepo,
        node_settings: NodeSettings
    ) -> None:
        self._find_node_use_case = find_node_use_case
        self._node_client = node_client
        self._peer_repo = peer_repo
        self._message_repo = message_repo
        self._settings = node_settings

    async def execute(self, source: UniversalPeerIdentifier, target: UniversalPeerIdentifier, content: str) -> None:
        if target.node != self._settings.IDENTIFIER:
            await self._node_client.send_message(
                await self._find_node_use_case.execute(target.node),
                source,
                target,
                content
            )
        elif not await self._peer_repo.exists(target.peer):
            raise DoesNotExist
        else:
            await self._message_repo.create(source, target.peer, content)
