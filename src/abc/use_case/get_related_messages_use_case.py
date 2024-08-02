from abc import ABC, abstractmethod

from src.type.internal import PeerCredentials, UniversalPeerIdentifier
from src.type.entity import Message


class GetRelatedMessagesUseCase(ABC):

    @abstractmethod
    async def execute(self, identifier: UniversalPeerIdentifier, credentials: PeerCredentials) -> list[Message]: ...
