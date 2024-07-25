from abc import ABC, abstractmethod

from src.type.entity import Message
from src.type.internal import PeerIdentifier, UniversalPeerIdentifier


class IMessageRepo(ABC):

    @abstractmethod
    async def relative_to_target(self, identifier: PeerIdentifier) -> list[Message]: ...

    @abstractmethod
    async def create(self, source: UniversalPeerIdentifier, target: PeerIdentifier, content: str) -> None: ...
