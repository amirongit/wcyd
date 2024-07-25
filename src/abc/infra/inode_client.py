from abc import ABC, abstractmethod

from src.type.internal import EndPoint, NodeIdentifier, UniversalPeerIdentifier
from src.type.entity import Node, Peer


class INodeClient(ABC):

    @abstractmethod
    async def connect_node(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def find_node(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node: ...

    @abstractmethod
    async def find_peer(self, host: Node, identifier: UniversalPeerIdentifier) -> Peer: ...

    @abstractmethod
    async def send_message(
        self,
        host: Node,
        source: UniversalPeerIdentifier,
        target: UniversalPeerIdentifier,
        content: str
    ) -> None: ...
