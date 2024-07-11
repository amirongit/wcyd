from src.abc.infra.ipeer_repo import IPeerRepo
from src.abc.use_case.remove_peer_use_case import RemovePeerUseCase
from src.type.internal import PeerIdentifier


class RemovePeer(RemovePeerUseCase):
    def __init__(self, peer_repo: IPeerRepo) -> None:
        self._peer_repo = peer_repo

    async def execute(self, identifier: PeerIdentifier) -> None:
        await self._peer_repo.delete(identifier)
