from abc import ABC, abstractmethod

from src.type.internal import Keyring, PeerIdentifier


class AddPeerUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: PeerIdentifier, public_key: Keyring) -> None: ...
