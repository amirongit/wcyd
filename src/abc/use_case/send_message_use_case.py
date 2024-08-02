from abc import ABC, abstractmethod

from src.type.internal import PeerCredentials, UniversalPeerIdentifier


class SendMessageUseCase(ABC):

    @abstractmethod
    async def execute(
        self,
        source: UniversalPeerIdentifier,
        target: UniversalPeerIdentifier,
        content: str,
        credentials: PeerCredentials
    ) -> None: ...
