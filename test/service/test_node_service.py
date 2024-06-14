from unittest import IsolatedAsyncioTestCase

from pydantic.networks import AnyUrl

from src.service.node_service import NodeService
from src.settings import NodeSettings
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.utils import create_far_neighbor


TEST_NODE_SETTINGS = NodeSettings(
    IDENTIFIER='test-node',
    ENDPOINT='http://localhost:44777', # type: ignore
    PUBLIC_KEY='PGP OR SSH PUB KEY IDK'
)


class TestNodeService(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self._node_service = NodeService(TEST_NODE_SETTINGS, MockNodeRepo(), MockNodeClient())

    def test_local_node(self) -> None:
        self.assertEqual(self._node_service.local_node.identifier, TEST_NODE_SETTINGS.IDENTIFIER)
        self.assertEqual(self._node_service.local_node.endpoint, TEST_NODE_SETTINGS.ENDPOINT)
        self.assertEqual(self._node_service.local_node.public_key, TEST_NODE_SETTINGS.PUBLIC_KEY)

    async def test_get_neighbors(self) -> None:
        with self.subTest():
            neighbors = await self._node_service.get_neighbors()
            self.assertEqual(len(neighbors), 0)

        with self.subTest():
            await self._node_service.connect('test-neighbor', AnyUrl('http://neighbor:80'), 'PUB KEY')
            neighbors = await self._node_service.get_neighbors()
            self.assertEqual(len(neighbors), 1)

    async def test_connect(self) -> None:
        neighbor_identifier = 'test-neighbor'
        neighbor_endpoint = AnyUrl('http://neighbor:80')
        neighbor_public_key = 'PUB KEY'
        await self._node_service.connect(neighbor_identifier, neighbor_endpoint, neighbor_public_key)

        with self.assertRaises(AlreadyExists):
            await self._node_service.connect(neighbor_identifier, neighbor_endpoint, neighbor_public_key)

        with self.subTest():
            neighbors = await self._node_service.get_neighbors()

            self.assertEqual(len(neighbors), 1)
            self.assertEqual(neighbors[0].identifier, neighbor_identifier)
            self.assertEqual(neighbors[0].endpoint, neighbor_endpoint)
            self.assertEqual(neighbors[0].public_key, neighbor_public_key)

    async def test_find(self) -> None:
        with self.assertRaises(AlreadyAnswered):
            await self._node_service.find({TEST_NODE_SETTINGS.IDENTIFIER}, 'test-node')

        neighbor_identifier = 'test-neighbor'
        neighbor_endpoint = AnyUrl('http://neighbor:80')
        neighbor_public_key = 'PUB KEY'
        await self._node_service.connect(neighbor_identifier, neighbor_endpoint, neighbor_public_key)

        with self.subTest():
            direct_neighbors = await self._node_service.get_neighbors()
            self.assertIn(neighbor_identifier, [n.identifier for n in direct_neighbors])

        with self.subTest():
            found_node = await self._node_service.find({'another-test-neighbor'}, neighbor_identifier)

            self.assertEqual(found_node.identifier, neighbor_identifier)
            self.assertEqual(found_node.endpoint, neighbor_endpoint)
            self.assertEqual(found_node.public_key, neighbor_public_key)

        far_neighbor_identifier = 'test-far-neighbor'
        far_neighbor_endpoint = AnyUrl('http://far-neighbor:80')
        far_neighbor_public_key = 'PUB KEY GPG'
        create_far_neighbor(
            self._node_service,
            neighbor_identifier,
            far_neighbor_identifier,
            far_neighbor_endpoint,
            far_neighbor_public_key
        )


        with self.subTest():
            direct_neighbors = await self._node_service.get_neighbors()
            self.assertNotIn(far_neighbor_identifier, [n.identifier for n in direct_neighbors])

        with self.subTest():
            found_node = await self._node_service.find({'another-test-neighbor'}, far_neighbor_identifier)

            self.assertEqual(found_node.identifier, far_neighbor_identifier)
            self.assertEqual(found_node.endpoint, far_neighbor_endpoint)
            self.assertEqual(found_node.public_key, far_neighbor_public_key)

        with self.assertRaises(NotFound):
            await self._node_service.find({'test-neighbor'}, 'not-existing-node')
