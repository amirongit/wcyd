from unittest import IsolatedAsyncioTestCase

from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists
from src.type.internal import PublicKey
from src.use_case.add_peer import AddPeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import get_peer


class TestAddPeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = (
        'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID0iYhOGZpnxtQSsndBmFatEY2D8vfb7n2h/PwiOyI4J '
        'root@5148f6a8c395'
    )

    def setUp(self) -> None:
        self._peer_repo = MockPeerRepo()
        self._add_peer_use_case = AddPeer(self._peer_repo)

    async def test_normal(self) -> None:
        test_peer_identifier = 'test-peer-identifier'

        await self._add_peer_use_case.execute(
            test_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        peer = get_peer(self._peer_repo, test_peer_identifier, 'not-being-tested')

        self.assertEqual(peer.identifier.peer, test_peer_identifier)
        self.assertEqual(peer.public_key.provider, AsymmetricCryptographyProvider.SSH)
        self.assertEqual(peer.public_key.value, self.SAMPLE_PUBLIC_KEY_VALUE)

    async def test_duplicated_identifier(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'
        await self._add_peer_use_case.execute(
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        with self.assertRaises(AlreadyExists):
            await self._add_peer_use_case.execute(
                existing_peer_identifier,
                PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
            )
