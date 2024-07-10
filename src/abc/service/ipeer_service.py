from abc import ABC, abstractmethod

from src.type.internal import PeerIdentifier, PublicKey


class IPeerService(ABC):

    @abstractmethod
    async def add(self, identifier: PeerIdentifier, public_key: PublicKey) -> None: ...

    @abstractmethod
    async def remove(self, identifier: PeerIdentifier) -> None: ...
