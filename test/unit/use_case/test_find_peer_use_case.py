from test.unit.mock.infra.mock_node_client import MockNodeClient
from test.unit.mock.infra.mock_node_repo import MockNodeRepo
from test.unit.mock.infra.mock_peer_repo import MockPeerRepo
from test.unit.utils import add_external_peer, add_internal_neighbor, add_internal_peer
from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.internal import Keyring, UniversalPeerIdentifier
from src.use_case.find_node import FindNode
from src.use_case.find_peer import FindPeer


class TestFindPeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_SIGNING_KEY = "QW1j319IkhjIGVmOBZAJt0Tsqs6d4nWbA5n6l1iupj8="
    SAMPLE_ENCRYPTION_KEY = "Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o="

    def setUp(self) -> None:
        self._settings = NodeSettings(IDENTIFIER="test-node", ENDPOINT=AnyUrl("http://localhost:44777"))
        self._mock_node_client = MockNodeClient()
        self._mock_peer_repo = MockPeerRepo(self._settings)
        self._mock_node_repo = MockNodeRepo()
        self._find_node_use_case = FindNode(self._settings, self._mock_node_repo, self._mock_node_client)
        self._use_case = FindPeer(
            self._settings, self._mock_node_client, self._mock_peer_repo, self._find_node_use_case
        )

    async def test_normal(self) -> None:
        existing_peer_identifier = "existing-peer-identifier"
        add_internal_peer(
            self._mock_peer_repo,
            existing_peer_identifier,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY),
        )

        peer = await self._use_case.execute(
            UniversalPeerIdentifier(node=self._settings.IDENTIFIER, peer=existing_peer_identifier)
        )

        self.assertEqual(peer.identifier.peer, existing_peer_identifier)
        self.assertEqual(peer.identifier.node, self._settings.IDENTIFIER)

    async def test_external(self) -> None:
        neighbor_identifier = "neighbor-identifier"
        add_internal_neighbor(self._mock_node_repo, neighbor_identifier, AnyUrl("http://not-being-tested:80"))

        external_peer_identifier = "external-peer-identifier"
        add_external_peer(
            self._mock_node_client,
            neighbor_identifier,
            external_peer_identifier,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY),
        )

        peer = await self._use_case.execute(
            UniversalPeerIdentifier(node=neighbor_identifier, peer=external_peer_identifier)
        )

        self.assertEqual(peer.identifier.node, neighbor_identifier)
        self.assertEqual(peer.identifier.peer, external_peer_identifier)
