from abc import ABC, abstractmethod

from src.type.entity import Peer
from src.type.internal import UniversalPeerIdentifier


class FindPeerUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: UniversalPeerIdentifier) -> Peer: ...
