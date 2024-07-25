from abc import ABC, abstractmethod

from src.type.entity import Message
from src.type.internal import UniversalPeerIdentifier


class IMessageRepo(ABC):

    @abstractmethod
    async def relative_to_target(self, identifier: UniversalPeerIdentifier) -> list[Message]: ...

    @abstractmethod
    async def create(self, source: UniversalPeerIdentifier, target: UniversalPeerIdentifier, content: str) -> None: ...
