from abc import ABC, abstractmethod

from src.type.entity import Message, Node, Peer
from src.type.internal import EndPoint, NodeIdentifier, PeerCredentials, UniversalPeerIdentifier


class INodeClient(ABC):

    @abstractmethod
    async def connect_node(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def find_node(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node: ...

    @abstractmethod
    async def find_peer(self, host: Node, identifier: UniversalPeerIdentifier) -> Peer: ...

    @abstractmethod
    async def send_message(
        self, host: Node, credentials: PeerCredentials, target: UniversalPeerIdentifier, content: str
    ) -> None: ...

    @abstractmethod
    async def get_related_messages(self, host: Node, credentials: PeerCredentials) -> list[Message]: ...
