from unittest import IsolatedAsyncioTestCase

from pydantic.networks import AnyUrl

from src.service.node_service import NodeService
from src.settings import NodeSettings
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.utils import create_far_neighbor


class TestNodeService(IsolatedAsyncioTestCase):

    TEST_NODE_SETTINGS = NodeSettings(
        IDENTIFIER='test-node',
        ENDPOINT=AnyUrl('http://localhost:44777')
    )

    def setUp(self) -> None:
        self._node_service = NodeService(TestNodeService.TEST_NODE_SETTINGS, MockNodeRepo(), MockNodeClient())

    def test_local_node(self) -> None:
        self.assertEqual(self._node_service.local_node.identifier, TestNodeService.TEST_NODE_SETTINGS.IDENTIFIER)
        self.assertEqual(self._node_service.local_node.endpoint, TestNodeService.TEST_NODE_SETTINGS.ENDPOINT)

    async def test_connect(self) -> None:
        neighbor_identifier = 'test-neighbor'
        neighbor_endpoint = AnyUrl('http://neighbor:80')
        await self._node_service.connect(neighbor_identifier, neighbor_endpoint)

        with self.assertRaises(AlreadyExists):
            await self._node_service.connect(neighbor_identifier, neighbor_endpoint)

        with self.subTest():
            neighbor = await self._node_service.find({'an-stranger'}, neighbor_identifier)

            self.assertEqual(neighbor.identifier, neighbor_identifier)
            self.assertEqual(neighbor.endpoint, neighbor_endpoint)

    async def test_find(self) -> None:
        with self.assertRaises(AlreadyAnswered):
            await self._node_service.find({TestNodeService.TEST_NODE_SETTINGS.IDENTIFIER}, 'test-node')

        neighbor_identifier = 'test-neighbor'
        neighbor_endpoint = AnyUrl('http://neighbor:80')
        await self._node_service.connect(neighbor_identifier, neighbor_endpoint)

        with self.subTest():
            found_node = await self._node_service.find({'another-test-neighbor'}, neighbor_identifier)

            self.assertEqual(found_node.identifier, neighbor_identifier)
            self.assertEqual(found_node.endpoint, neighbor_endpoint)

        far_neighbor_identifier = 'test-far-neighbor'
        far_neighbor_endpoint = AnyUrl('http://far-neighbor:80')
        create_far_neighbor(
            self._node_service,
            neighbor_identifier,
            far_neighbor_identifier,
            far_neighbor_endpoint,
        )

        with self.subTest():
            found_node = await self._node_service.find({'another-test-neighbor'}, far_neighbor_identifier)

            self.assertEqual(found_node.identifier, far_neighbor_identifier)
            self.assertEqual(found_node.endpoint, far_neighbor_endpoint)

        with self.assertRaises(NotFound):
            await self._node_service.find({'test-neighbor'}, 'not-existing-node')
