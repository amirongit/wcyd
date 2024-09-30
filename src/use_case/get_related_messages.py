from src.abc.infra.imessage_repo import IMessageRepo
from src.abc.infra.inode_client import INodeClient
from src.abc.infra.ipeer_repo import IPeerRepo
from src.abc.use_case.find_node_use_case import FindNodeUseCase
from src.abc.use_case.get_related_messages_use_case import GetRelatedMessagesUseCase
from src.settings import NodeSettings
from src.type.entity import Message
from src.type.internal import PeerCredentials, UniversalPeerIdentifier


class GetRelatedMessages(GetRelatedMessagesUseCase):
    def __init__(
        self,
        find_node_use_case: FindNodeUseCase,
        peer_repo: IPeerRepo,
        message_repo: IMessageRepo,
        node_client: INodeClient,
        node_settings: NodeSettings,
    ) -> None:
        self._find_node_use_case = find_node_use_case
        self._peer_repo = peer_repo
        self._message_repo = message_repo
        self._client = node_client
        self._settings = node_settings

    async def execute(self, identifier: UniversalPeerIdentifier, credentials: PeerCredentials) -> list[Message]:
        if identifier.node != self._settings.IDENTIFIER:
            return await self._client.get_related_messages(
                await self._find_node_use_case.execute(identifier.node), credentials
            )

        return await self._message_repo.relative_to_target(identifier.peer)
