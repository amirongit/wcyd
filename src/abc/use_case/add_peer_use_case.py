from abc import ABC, abstractmethod

from src.type.internal import PeerIdentifier, PublicKey


class AddPeerUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: PeerIdentifier, public_key: PublicKey) -> None: ...
