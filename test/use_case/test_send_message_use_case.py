from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.exception import DoesNotExist
from src.type.internal import Keyring, UniversalPeerIdentifier
from src.use_case.find_node import FindNode
from src.use_case.send_message import SendMessage
from test.mock.infra.mock_message_repo import MockMessageRepo
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import (
    add_external_peer,
    add_internal_neighbor,
    add_internal_peer,
    get_external_relative_messages,
    get_internal_relative_messages
)


class TestSendMessageUseCase(IsolatedAsyncioTestCase):

    SAMPLE_SIGNING_KEY = 'QW1j319IkhjIGVmOBZAJt0Tsqs6d4nWbA5n6l1iupj8='
    SAMPLE_ENCRYPTION_KEY = 'Ov4eCC6vqpcBbswXLfn0aRD9TvafYB+BVprg7eyv03o='
    EXISTING_PEER_IDENTIFIER = 'existing-peer-identifier'
    EXISTING_NEIGHBOR_IDENTIFIER = 'existing-neighbor-identifier'
    EXTERNAL_PEER_IDENTIFIER = 'external-peer-identifier'

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._mock_node_client = MockNodeClient()
        self._mock_message_repo = MockMessageRepo(self._settings)
        self._mock_node_repo = MockNodeRepo()
        self._mock_peer_repo = MockPeerRepo(self._settings)
        self._find_node_use_case = FindNode(self._settings, self._mock_node_repo, self._mock_node_client)
        add_internal_peer(
            self._mock_peer_repo,
            self.EXISTING_PEER_IDENTIFIER,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY)
        )
        add_internal_neighbor(
            self._mock_node_repo,
            self.EXISTING_NEIGHBOR_IDENTIFIER,
            AnyUrl('http://not-being-tested:80')
        )
        add_external_peer(
            self._mock_node_client,
            self.EXISTING_NEIGHBOR_IDENTIFIER,
            self.EXTERNAL_PEER_IDENTIFIER,
            Keyring(signing=self.SAMPLE_SIGNING_KEY, encryption=self.SAMPLE_ENCRYPTION_KEY)
        )
        self._use_case = SendMessage(
            self._find_node_use_case,
            self._mock_node_client,
            self._mock_message_repo,
            self._mock_peer_repo,
            self._settings
        )

    async def test_normal(self) -> None:
        source_node = 'source-node'
        source_peer = 'source-peer'
        content = 'sample content'

        await self._use_case.execute(
            UniversalPeerIdentifier(node=source_node, peer=source_peer),
            UniversalPeerIdentifier(node=self._settings.IDENTIFIER, peer=self.EXISTING_PEER_IDENTIFIER),
            content
        )

        messages = await get_internal_relative_messages(self._mock_message_repo, self.EXISTING_PEER_IDENTIFIER)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, content)
        self.assertEqual(messages[0].source.node, source_node)
        self.assertEqual(messages[0].source.peer, source_peer)

    async def test_absent_identifier(self) -> None:
        with self.assertRaises(DoesNotExist):
            await self._use_case.execute(
                UniversalPeerIdentifier(node='not-being-tested', peer='not-being-tested'),
                UniversalPeerIdentifier(node=self._settings.IDENTIFIER, peer='absent-identifier'),
                'not-being-tested'
            )

    async def test_external_peer(self) -> None:
        source_node = 'source-node'
        source_peer = 'source-peer'
        target = UniversalPeerIdentifier(node=self.EXISTING_NEIGHBOR_IDENTIFIER, peer=self.EXTERNAL_PEER_IDENTIFIER)
        content = 'sample content'

        await self._use_case.execute(UniversalPeerIdentifier(node=source_node, peer=source_peer), target, content)

        messages = get_external_relative_messages(self._mock_node_client, target)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].content, content)
        self.assertEqual(messages[0].source.node, source_node)
        self.assertEqual(messages[0].source.peer, source_peer)
