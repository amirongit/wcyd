from src.abc.infra.inode_client import INodeClient
from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node


class NodeClient(INodeClient):

    async def get_neighbors(self, host: Node) -> set[Identifier]: ...

    async def connect(self, host: Node, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None: ...

    async def find(self, host: Node, questioners: set[Identifier], identifier: Identifier) -> Node: ...
