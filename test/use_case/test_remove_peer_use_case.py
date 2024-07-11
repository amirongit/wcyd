from unittest import IsolatedAsyncioTestCase

from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import DoesNotExist
from src.type.internal import PublicKey
from src.use_case.remove_peer import RemovePeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import add_peer


class TestRemovePeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = (
        'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID0iYhOGZpnxtQSsndBmFatEY2D8vfb7n2h/PwiOyI4J '
        'root@5148f6a8c395'
    )

    def setUp(self) -> None:
        self._peer_repo = MockPeerRepo()
        self._remove_peer_use_case = RemovePeer(self._peer_repo)

    async def test_absent_identifier(self) -> None:
        absent_peer_identifier = 'absent-peer-identifier'

        with self.assertRaises(DoesNotExist):
            await self._remove_peer_use_case.execute(absent_peer_identifier)

    async def test_normal(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'

        add_peer(
            self._peer_repo,
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        await self._remove_peer_use_case.execute(existing_peer_identifier)
