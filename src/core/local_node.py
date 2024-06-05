from typing import NoReturn, Coroutine, Self

from src.abc.core.inode import INode
from src.type.dto import ChannelDTO
from src.type.alias import Identifier, PublicKey
from src.type.exception import AlreadyAnswered, AlreadyConnected, NotFound


class LocalNode(INode):
    def __init__(self, identifier: Identifier, public_key: PublicKey, endpoint: str):
        self._channel = ChannelDTO(endpoint=endpoint, public_key=public_key) # type: ignore
        self._identifier = identifier
        self._neighbors: dict[Identifier, INode] = dict()

    @property
    def channel(self) -> ChannelDTO:
        return self._channel

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    @property
    def neighbors(self) -> Coroutine[Self, NoReturn, set[Identifier]]:
        async def awaitable(self) -> set[Identifier]:
            return set(self._neighbors.keys())
        return awaitable(self)

    async def connect(self, node: INode) -> None:
        if node.identifier in await self.neighbors:
            raise AlreadyConnected

        self._neighbors[node.identifier] = node

        try:
            await node.connect(self)
        except AlreadyConnected:
            pass

    async def find(self, questioners: set[Identifier], identifier: Identifier) -> INode:
        if self.identifier in questioners:
            raise AlreadyAnswered

        if (immediate := self._neighbors.get(identifier)) is not None:
            return immediate

        new_questioners = questioners | {self.identifier}
        for immediate in {v for k, v in self._neighbors.items() if k not in questioners}:
            try:
                return await immediate.find(new_questioners, identifier)
            except NotFound:
                new_questioners |= {immediate.identifier}

        raise NotFound