from abc import ABC, abstractmethod

from src.type.entity import Node
from src.type.internal import EndPoint, NodeIdentifier


class INodeRepo(ABC):

    @abstractmethod
    async def get(self, identifier: NodeIdentifier) -> Node: ...

    @abstractmethod
    async def exists(self, identifier: NodeIdentifier) -> bool: ...

    @abstractmethod
    async def create(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def all(self) -> list[Node]: ...
