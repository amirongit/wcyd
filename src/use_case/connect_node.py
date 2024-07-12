from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.abc.use_case.connect_node_use_case import ConnectNodeUseCase
from src.settings import NodeSettings
from src.type.exception import AlreadyExists
from src.type.internal import EndPoint, NodeIdentifier


class ConnectNode(ConnectNodeUseCase):
    def __init__(self, node_settings: NodeSettings, node_repo: INodeRepo, node_client: INodeClient) -> None:
        self._settings = node_settings
        self._node_repo = node_repo
        self._node_client = node_client

    async def execute(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        await self._node_repo.create(identifier, endpoint)

        try:
            await self._node_client.connect_node(
                await self._node_repo.get(identifier),
                self._settings.IDENTIFIER,
                self._settings.ENDPOINT
            )
        except AlreadyExists:
            pass
