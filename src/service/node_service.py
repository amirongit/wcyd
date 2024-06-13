from src.abc.service.inode_service import INodeService
from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, AlreadyConnected, NotFound

from src.settings import Settings


class NodeService(INodeService):
    def __init__(self, settings: Settings, node_repo: INodeRepo, node_client: INodeClient):
        self._local_node = Node(
            identifier=settings.LOCAL_NODE.IDENTIFIER,
            endpoint=settings.LOCAL_NODE.ENDPOINT,
            public_key=settings.LOCAL_NODE.PUBLIC_KEY
        )
        self._node_repo = node_repo
        self._node_client = node_client

    @property
    def local_node(self) -> Node:
        return self._local_node

    async def get_neighbors(self) -> list[Node]:
        return await self._node_repo.all()

    async def connect(self, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None:
        if await self._node_repo.exists(identifier):
            raise AlreadyConnected

        await self._node_repo.create(identifier, endpoint, public_key)

        try:
            await self._node_client.connect(
                await self._node_repo.get(identifier),
                self.local_node.identifier,
                self.local_node.endpoint,
                self.local_node.public_key,
            )
        except AlreadyConnected:
            pass

    async def find(self, questioners: set[Identifier], identifier: Identifier) -> Node:
        if self.local_node.identifier in questioners:
            raise AlreadyAnswered

        try:
            return await self._node_repo.get(identifier)
        except NotFound:
            new_questioners = questioners | {self.local_node.identifier}
            for node in await self.get_neighbors():
                try:
                    return await self._node_client.find(node, new_questioners, identifier)
                except (NotFound, AlreadyAnswered):
                    new_questioners.add(node.identifier)

        raise NotFound
