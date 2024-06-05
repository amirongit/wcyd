from typing import NoReturn, Coroutine, Self

from src.abc.core.inode import INode
from src.abc.infra.inode_client import INodeClient
from src.type.alias import Identifier, PublicKey
from src.type.dto import ChannelDTO


class RemoteNode(INode):
    def __init__(self, identifier: Identifier, public_key: PublicKey, endpoint: str, client: INodeClient):
        self._channel = ChannelDTO(endpoint=endpoint, public_key=public_key) # type: ignore
        self._identifier = identifier
        self._client = client

    @property
    def channel(self) -> ChannelDTO:
        return self._channel

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    @property
    def neighbors(self) -> Coroutine[Self, NoReturn, set[Identifier]]:
        return self._client.get_neighbors(self._channel)

    async def connect(self, node: INode) -> None:
        await self._client.connect_node(node.channel)

    async def find(self, questioners: set[Identifier], identifier: Identifier) -> INode:
        return await self._client.find_node(questioners, identifier)
