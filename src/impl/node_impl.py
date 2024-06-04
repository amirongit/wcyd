from src.abc.node import Node
from src.type import ChannelDTO, Identifier, NodeAlreadyAnswered, NodeAlreadyIsConnected, NodeNotFound, PublicKey


class NodeImpl(Node):
    def __init__(self, identifier: Identifier, public_key: PublicKey, endpoint: str):
        self._channel: ChannelDTO = ChannelDTO(endpoint=endpoint, public_key=public_key) # type: ignore
        self._identifier: Identifier = identifier
        self._neighbors: dict[Identifier, Node] = dict()

    @property
    def channel(self) -> ChannelDTO:
        return self._channel

    @property
    def identifier(self) -> Identifier:
        return self._identifier

    @property
    def neighbors(self) -> set[Identifier]:
        return set(self._neighbors.keys())

    def connect(self, node: Node) -> None:
        if node.identifier in self.neighbors:
            raise NodeAlreadyIsConnected

        self._neighbors[node.identifier] = node

        try:
            node.connect(self)
        except NodeAlreadyIsConnected:
            return

    def find(self, questioners: set[Identifier], identifier: Identifier) -> Node:
        if self.identifier in questioners:
            raise NodeAlreadyAnswered

        if (immediate := self._neighbors.get(identifier)) is not None:
            return immediate

        new_questioners = questioners | {self.identifier}
        for immediate in {v for k, v in self._neighbors.items() if k not in questioners}:
            try:
                return immediate.find(questioners, identifier)
            except NodeNotFound:
                continue

        raise NodeNotFound

