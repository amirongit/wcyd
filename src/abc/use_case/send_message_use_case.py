from abc import ABC, abstractmethod

from src.type.internal import UniversalPeerIdentifier


class SendMessageUseCase(ABC):

    @abstractmethod
    async def execute(self, source: UniversalPeerIdentifier, target: UniversalPeerIdentifier, content: str) -> None: ...
