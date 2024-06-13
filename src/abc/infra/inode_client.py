from __future__ import annotations

from abc import ABC, abstractmethod

from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node


class INodeClient(ABC):

    @abstractmethod
    async def get_neighbors(self, host: Node) -> set[Identifier]: ...

    @abstractmethod
    async def connect(self, host: Node, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None: ...

    @abstractmethod
    async def find(self, host: Node, questioners: set[Identifier], identifier: Identifier) -> Node: ...
