from abc import ABC, abstractmethod

from src.type.internal import EndPoint, NodeIdentifier
from src.type.entity import Node


class INodeService(ABC):

    @property
    @abstractmethod
    def local_node(self) -> Node: ...

    @abstractmethod
    async def connect(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def find(self, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node: ...
