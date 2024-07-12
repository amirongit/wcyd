from src.abc.infra.inode_client import INodeClient
from src.abc.infra.ipeer_repo import IPeerRepo
from src.abc.use_case.find_peer_use_case import FindPeerUseCase
from src.abc.use_case.find_node_use_case import FindNodeUseCase
from src.settings import NodeSettings
from src.type.entity import Peer
from src.type.internal import UniversalPeerIdentifier


class FindPeer(FindPeerUseCase):
    def __init__(
        self,
        node_settings: NodeSettings,
        node_client: INodeClient,
        peer_repo: IPeerRepo,
        find_node_use_case: FindNodeUseCase,
    ) -> None:
        self._settings = node_settings
        self._node_client = node_client
        self._find_node_use_case = find_node_use_case
        self._peer_repo = peer_repo

    async def execute(self, identifier: UniversalPeerIdentifier) -> Peer:
        if identifier.node == self._settings.IDENTIFIER:
            return await self._peer_repo.get(identifier.peer)

        return await self._node_client.find_peer(
            await self._find_node_use_case.execute({self._settings.IDENTIFIER}, identifier.node),
            identifier
        )
