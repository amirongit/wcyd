from __future__ import annotations

from abc import ABC, abstractmethod

from src.type.alias import EndPoint, Identifier
from src.type.entity import Node


class INodeService(ABC):

    @property
    @abstractmethod
    def local_node(self) -> Node: ...

    @abstractmethod
    async def get_neighbors(self) -> list[Node]: ...

    @abstractmethod
    async def connect(self, identifier: Identifier, endpoint: EndPoint) -> None: ...

    @abstractmethod
    async def find(self, questioners: set[Identifier], identifier: Identifier) -> Node: ...
