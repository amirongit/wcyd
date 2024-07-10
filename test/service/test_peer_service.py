from unittest import IsolatedAsyncioTestCase

from src.service.peer_service import PeerService
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import PublicKey
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import get_peer


class TestPeerService(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = (
        'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAID0iYhOGZpnxtQSsndBmFatEY2D8vfb7n2h/PwiOyI4J '
        'root@5148f6a8c395'
    )

    def setUp(self) -> None:
        self._peer_service = PeerService(MockPeerRepo())

    async def test_add(self) -> None:
        test_peer_identifier = 'test-add-peer'

        with self.subTest():
            await self._peer_service.add(
                test_peer_identifier,
                PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
            )

            peer = get_peer(self._peer_service, test_peer_identifier, 'not-being-tested')

            self.assertEqual(peer.identifier.peer, test_peer_identifier)
            self.assertEqual(peer.public_key.provider, AsymmetricCryptographyProvider.SSH)
            self.assertEqual(peer.public_key.value, self.SAMPLE_PUBLIC_KEY_VALUE)

        with self.subTest():
            with self.assertRaises(AlreadyExists):
                await self._peer_service.add(
                    test_peer_identifier,
                    PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
                )

    async def test_remove(self) -> None:
        peer_identifier = 'test-remove-peer'

        with self.subTest():
            with self.assertRaises(DoesNotExist):
                await self._peer_service.remove(peer_identifier)


        await self._peer_service.add(
            peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.SSH, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        with self.subTest():
            await self._peer_service.remove(peer_identifier)
