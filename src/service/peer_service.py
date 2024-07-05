from src.abc.service.ipeer_service import IPeerService
from src.abc.infra.ipeer_repo import IPeerRepo
from src.type.internal import PeerIdentifier, PublicKey


class PeerService(IPeerService):
    def __init__(self, peer_repo: IPeerRepo):
        self._peer_repo = peer_repo

    async def add(self, identifier: PeerIdentifier, public_key: PublicKey) -> None:
        await self._peer_repo.create(identifier, public_key)

    async def remove(self, identifier: PeerIdentifier) -> None:
        await self._peer_repo.delete(identifier)
