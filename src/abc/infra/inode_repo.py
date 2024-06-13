from abc import ABC, abstractmethod

from src.type.entity import Node
from src.type.alias import EndPoint, Identifier, PublicKey


class INodeRepo(ABC):

    @abstractmethod
    async def get(self, identifier: Identifier) -> Node: ...

    @abstractmethod
    async def exists(self, identifier: Identifier) -> bool: ...

    @abstractmethod
    async def create(self, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None: ...

    @abstractmethod
    async def all(self) -> list[Node]: ...
