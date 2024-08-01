from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.exception import AlreadyExists
from src.type.internal import Keyring
from src.use_case.add_peer import AddPeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import get_internal_peer


class TestAddPeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_SIGNING_KEY = 'QW1j319IkhjIGVmOBZAJt0Tsqs6d4nWbA5n6l1iupj8='
    SAMPLE_ENCRYPTION_KEY = 'Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o='

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
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY)
        )

        peer = await get_internal_peer(self._peer_repo, test_peer_identifier)

        self.assertEqual(peer.identifier.peer, test_peer_identifier)
        self.assertEqual(peer.keyring.signing, self.SAMPLE_SIGNING_KEY)
        self.assertEqual(peer.keyring.encryption, self.SAMPLE_ENCRYPTION_KEY)

    async def test_duplicated_identifier(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'
        await self._use_case.execute(
            existing_peer_identifier,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY)
        )

        with self.assertRaises(AlreadyExists):
            await self._use_case.execute(
                existing_peer_identifier,
                Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY)
            )
