from abc import ABC, abstractmethod

from src.type.internal import EndPoint, NodeIdentifier
from src.type.entity import Node


class INodeClient(ABC):

    @abstractmethod
    async def get_neighbors(self, host: Node) -> list[Node]: ...

    @abstractmethod
    async def connect(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def find(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node: ...
