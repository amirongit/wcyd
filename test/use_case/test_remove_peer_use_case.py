from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import DoesNotExist
from src.type.internal import PublicKey
from src.use_case.remove_peer import RemovePeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import add_internal_peer


class TestRemovePeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = 'Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o='

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._peer_repo = MockPeerRepo(self._settings)
        self._use_case = RemovePeer(self._peer_repo)

    async def test_absent_identifier(self) -> None:
        absent_peer_identifier = 'absent-peer-identifier'

        with self.assertRaises(DoesNotExist):
            await self._use_case.execute(absent_peer_identifier)

    async def test_normal(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'

        add_internal_peer(
            self._peer_repo,
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.NACL, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        await self._use_case.execute(existing_peer_identifier)
