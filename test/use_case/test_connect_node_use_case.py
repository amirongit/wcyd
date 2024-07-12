from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.exception import AlreadyExists
from src.use_case.connect_node import ConnectNode
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.utils import get_node


class TestConnectNodeUseCase(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._mock_node_client = MockNodeClient()
        self._mock_node_repo = MockNodeRepo()
        self._use_case = ConnectNode(self._settings, self._mock_node_repo, self._mock_node_client)

    async def test_duplicated_identifier(self) -> None:
        existing_neighbor_identifier = 'existing-neighbor-identifier'
        endpoint = AnyUrl('http://existing-neighbor:80')
        await self._use_case.execute(existing_neighbor_identifier, endpoint)

        with self.assertRaises(AlreadyExists):
            await self._use_case.execute(existing_neighbor_identifier, endpoint)

    async def test_normal(self) -> None:
        test_neighbor_identifier = 'test-neighbor-identifier'
        endpoint = AnyUrl('http://test-neighbor:80')
        await self._use_case.execute(test_neighbor_identifier, endpoint)

        neighbor = get_node(self._mock_node_repo, test_neighbor_identifier)

        self.assertEqual(neighbor.identifier, test_neighbor_identifier)
        self.assertEqual(neighbor.endpoint, endpoint)
