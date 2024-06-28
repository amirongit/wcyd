from src.abc.service.inode_service import INodeService
from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.type.internal import EndPoint, NodeIdentifier
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound

from src.settings import NodeSettings


class NodeService(INodeService):
    def __init__(self, node_settings: NodeSettings, node_repo: INodeRepo, node_client: INodeClient) -> None:
        self._local_node = Node(
            identifier=node_settings.IDENTIFIER,
            endpoint=node_settings.ENDPOINT,
        )
        self._node_repo = node_repo
        self._node_client = node_client

    @property
    def local_node(self) -> Node:
        return self._local_node

    async def connect(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        await self._node_repo.create(identifier, endpoint)

        try:
            await self._node_client.connect(
                await self._node_repo.get(identifier),
                self.local_node.identifier,
                self.local_node.endpoint,
            )
        except AlreadyExists:
            pass

    async def find(self, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        if self.local_node.identifier in questioners:
            raise AlreadyAnswered

        try:
            return await self._node_repo.get(identifier)
        except NotFound:
            new_questioners = questioners | {self.local_node.identifier}
            for node in await self._node_repo.all():
                try:
                    return await self._node_client.find(node, new_questioners, identifier)
                except (NotFound, AlreadyAnswered):
                    new_questioners.add(node.identifier)

        raise NotFound
