from src.abc.core.inode import INode
from src.type import ChannelDTO, Identifier, AlreadyAnswered, AlreadyConnected, NotFound, PublicKey


class Node(INode):
    def __init__(self, identifier: Identifier, public_key: PublicKey, endpoint: str):
        self._channel: ChannelDTO = ChannelDTO(endpoint=endpoint, public_key=public_key) # type: ignore
        self._identifier: Identifier = identifier
        self._neighbors: dict[Identifier, INode] = dict()

    @property
    def channel(self) -> ChannelDTO:
        return self._channel

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    @property
    def neighbors(self) -> set[Identifier]:
        return set(self._neighbors.keys())

    def connect(self, node: INode) -> None:
        if node.identifier in self.neighbors:
            raise AlreadyConnected

        self._neighbors[node.identifier] = node

        try:
            node.connect(self)
        except AlreadyConnected:
            return

    def find(self, questioners: set[Identifier], identifier: Identifier) -> INode:
        if self.identifier in questioners:
            raise AlreadyAnswered

        if (immediate := self._neighbors.get(identifier)) is not None:
            return immediate

        new_questioners = questioners | {self.identifier}
        for immediate in {v for k, v in self._neighbors.items() if k not in questioners}:
            try:
                return immediate.find(new_questioners, identifier)
            except NotFound:
                new_questioners |= {immediate.identifier}

        raise NotFound

