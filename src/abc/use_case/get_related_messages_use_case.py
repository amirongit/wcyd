from abc import ABC, abstractmethod

from src.type.entity import Message
from src.type.internal import PeerCredentials, UniversalPeerIdentifier


class GetRelatedMessagesUseCase(ABC):

    @abstractmethod
    async def execute(self, identifier: UniversalPeerIdentifier, credentials: PeerCredentials) -> list[Message]: ...
