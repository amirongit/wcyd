from test.unit.mock.infra.mock_message_repo import MockMessageRepo
from test.unit.mock.infra.mock_node_client import MockNodeClient
from test.unit.mock.infra.mock_node_repo import MockNodeRepo
from test.unit.mock.infra.mock_peer_repo import MockPeerRepo
from test.unit.utils import (
    add_external_message,
    add_external_peer,
    add_internal_message,
    add_internal_neighbor,
    add_internal_peer,
    make_auth_credentials,
)
from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.internal import Keyring, UniversalPeerIdentifier
from src.use_case.find_node import FindNode
from src.use_case.get_related_messages import GetRelatedMessages


class TestSendMessageUseCase(IsolatedAsyncioTestCase):

    SAMPLE_SIGNING_KEY = "QW1j319IkhjIGVmOBZAJt0Tsqs6d4nWbA5n6l1iupj8="
    SAMPLE_ENCRYPTION_KEY = "Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o="
    EXISTING_NEIGHBOR_IDENTIFIER = "existing-neighbor-identifier"
    EXISTING_PEER_IDENTIFIER = "existing-peer-identifier"
    EXTERNAL_PEER_IDENTIFIER = "external-peer-identifier"

    def setUp(self) -> None:
        self._settings = NodeSettings(IDENTIFIER="test-node", ENDPOINT=AnyUrl("http://localhost:44777"))
        self._mock_node_client = MockNodeClient()
        self._mock_message_repo = MockMessageRepo(self._settings)
        self._mock_node_repo = MockNodeRepo()
        self._mock_peer_repo = MockPeerRepo(self._settings)
        self._find_node_use_case = FindNode(self._settings, self._mock_node_repo, self._mock_node_client)
        add_internal_neighbor(
            self._mock_node_repo, self.EXISTING_NEIGHBOR_IDENTIFIER, AnyUrl("http://not-being-tested")
        )
        add_external_peer(
            self._mock_node_client,
            self.EXISTING_NEIGHBOR_IDENTIFIER,
            self.EXTERNAL_PEER_IDENTIFIER,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY),
        )
        add_internal_peer(
            self._mock_peer_repo,
            self.EXISTING_PEER_IDENTIFIER,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY),
        )
        self._use_case = GetRelatedMessages(
            self._find_node_use_case,
            self._mock_peer_repo,
            self._mock_message_repo,
            self._mock_node_client,
            self._settings,
        )

    async def test_internal_message(self) -> None:
        content = "sample-content"
        source = UniversalPeerIdentifier(peer=self.EXTERNAL_PEER_IDENTIFIER, node=self.EXISTING_NEIGHBOR_IDENTIFIER)
        target = UniversalPeerIdentifier(peer=self.EXISTING_NEIGHBOR_IDENTIFIER, node=self._settings.IDENTIFIER)
        await add_internal_message(self._mock_message_repo, source, target.peer, content)

        messages = await self._use_case.execute(target, make_auth_credentials(target))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, content)
        self.assertEqual(messages[0].source.node, source.node)
        self.assertEqual(messages[0].source.peer, source.peer)
        self.assertEqual(messages[0].target.node, target.node)
        self.assertEqual(messages[0].target.peer, target.peer)

    async def test_external_message(self) -> None:
        content = "sample-content"
        target = UniversalPeerIdentifier(peer=self.EXTERNAL_PEER_IDENTIFIER, node=self.EXISTING_NEIGHBOR_IDENTIFIER)
        source = UniversalPeerIdentifier(peer=self.EXISTING_NEIGHBOR_IDENTIFIER, node=self._settings.IDENTIFIER)
        add_external_message(self._mock_node_client, source, target, content)

        messages = await self._use_case.execute(target, make_auth_credentials(target))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, content)
        self.assertEqual(messages[0].source.node, source.node)
        self.assertEqual(messages[0].source.peer, source.peer)
        self.assertEqual(messages[0].target.node, target.node)
        self.assertEqual(messages[0].target.peer, target.peer)
