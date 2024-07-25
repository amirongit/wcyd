from abc import ABC, abstractmethod

from src.type.entity import Peer
from src.type.internal import PeerIdentifier, PublicKey


class IPeerRepo(ABC):

    @abstractmethod
    async def get(self, identifier: PeerIdentifier) -> Peer: ...

    @abstractmethod
    async def exists(self, identifier: PeerIdentifier) -> bool: ...

    @abstractmethod
    async def create(self, identifier: PeerIdentifier, public_key: PublicKey) -> None: ...

    @abstractmethod
    async def delete(self, identifier: PeerIdentifier) -> None: ...
