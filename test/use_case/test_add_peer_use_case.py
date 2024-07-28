from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists
from src.type.internal import PublicKey
from src.use_case.add_peer import AddPeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import get_internal_peer


class TestAddPeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = 'Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o='

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._peer_repo = MockPeerRepo(self._settings)
        self._use_case = AddPeer(self._peer_repo)

    async def test_normal(self) -> None:
        test_peer_identifier = 'test-peer-identifier'

        await self._use_case.execute(
            test_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.NACL, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        peer = await get_internal_peer(self._peer_repo, test_peer_identifier)

        self.assertEqual(peer.identifier.peer, test_peer_identifier)
        self.assertEqual(peer.public_key.provider, AsymmetricCryptographyProvider.NACL)
        self.assertEqual(peer.public_key.value, self.SAMPLE_PUBLIC_KEY_VALUE)

    async def test_duplicated_identifier(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'
        await self._use_case.execute(
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.NACL, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        with self.assertRaises(AlreadyExists):
            await self._use_case.execute(
                existing_peer_identifier,
                PublicKey(provider=AsymmetricCryptographyProvider.NACL, value=self.SAMPLE_PUBLIC_KEY_VALUE)
            )
