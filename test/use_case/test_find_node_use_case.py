from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.exception import AlreadyAnswered, DoesNotExist
from src.use_case.find_node import FindNode
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.utils import add_node, add_far_neighbor


class TestFindNodeUseCase(IsolatedAsyncioTestCase):

    TEST_NODE_SETTINGS = NodeSettings(
        IDENTIFIER='test-node',
        ENDPOINT=AnyUrl('http://localhost:44777')
    )

    def setUp(self) -> None:
        self._mock_node_client = MockNodeClient()
        self._mock_node_repo = MockNodeRepo()
        self._use_case = FindNode(TestFindNodeUseCase.TEST_NODE_SETTINGS, self._mock_node_repo, self._mock_node_client)

    async def test_already_answered(self) -> None:
        with self.assertRaises(AlreadyAnswered):
            await self._use_case.execute({TestFindNodeUseCase.TEST_NODE_SETTINGS.IDENTIFIER}, 'not-being-tested')

    async def test_direct_neighbor(self) -> None:
        neighbor_identifier = 'neighbor-identifier'
        endpoint = AnyUrl('http://neighbor:80')
        add_node(self._mock_node_repo, neighbor_identifier, endpoint)

        node = await self._use_case.execute({'not-being-tested'}, neighbor_identifier)

        self.assertEqual(node.identifier, neighbor_identifier)
        self.assertEqual(node.endpoint, endpoint)

    async def test_far_neighbor(self) -> None:
        direct_neighbor_identifier = 'direct-neighbor-identifier'
        add_node(self._mock_node_repo, direct_neighbor_identifier, AnyUrl('http://not-bing-tested:80'))

        far_neighbor_identifier = 'far-neighbor-identifier'
        far_neighbor_endpoint = AnyUrl('http://far-neighbor:80')
        add_far_neighbor(
            self._mock_node_client,
            direct_neighbor_identifier,
            far_neighbor_identifier,
            far_neighbor_endpoint,
        )

        node = await self._use_case.execute({'not-being-tested'}, far_neighbor_identifier)

        self.assertEqual(node.identifier, far_neighbor_identifier)
        self.assertEqual(node.endpoint, far_neighbor_endpoint)

    async def test_absent_identifier(self) -> None:
        with self.assertRaises(DoesNotExist):
            await self._use_case.execute({'not-being-tested'}, 'absent-identifier')
