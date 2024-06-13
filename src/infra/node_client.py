from src.abc.infra.inode_client import INodeClient


class NodeClient(INodeClient):

    async def get_neighbors(self, host: Node) -> set[Identifier]: ...

    async def connect(self, host: Node, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None: ...

    async def find(self, host: Node, questioners: set[Identifier], identifier: Identifier) -> Node: ...
