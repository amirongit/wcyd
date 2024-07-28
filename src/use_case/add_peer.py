from src.abc.infra.ipeer_repo import IPeerRepo
from src.abc.use_case.add_peer_use_case import AddPeerUseCase
from src.type.internal import PeerIdentifier, Keyring


class AddPeer(AddPeerUseCase):
    def __init__(self, peer_repo: IPeerRepo) -> None:
        self._peer_repo = peer_repo

    async def execute(self, identifier: PeerIdentifier, public_key: Keyring) -> None:
        await self._peer_repo.create(identifier, public_key)
