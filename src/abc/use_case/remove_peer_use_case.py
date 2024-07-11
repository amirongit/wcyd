from abc import ABC, abstractmethod

from src.type.internal import PeerIdentifier


class RemovePeerUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: PeerIdentifier) -> None: ...
