from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.exception import AlreadyExists
from src.use_case.connect_node import ConnectNode
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.utils import get_internal_neighbor, add_internal_neighbor, add_external_neighbor


class TestConnectNodeUseCase(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._mock_node_client = MockNodeClient()
        self._mock_node_repo = MockNodeRepo()
        self._use_case = ConnectNode(self._settings, self._mock_node_repo, self._mock_node_client)

    async def test_internal_duplicated_identifier(self) -> None:
        internal_existing_neighbor_identifier = 'internal-existing-neighbor-identifier'
        endpoint = AnyUrl('http://internal-existing-neighbor:80')
        await self._use_case.execute(internal_existing_neighbor_identifier, endpoint)

        with self.assertRaises(AlreadyExists):
            await self._use_case.execute(internal_existing_neighbor_identifier, endpoint)

    async def test_external_duplicated_identifier(self) -> None:
        external_existing_neighbor_identifier = 'external-existing-neighbor-identifier'
        endpoint = AnyUrl('http://external-existing-neighbor:80')
        add_external_neighbor(self._mock_node_client, external_existing_neighbor_identifier, self._settings.IDENTIFIER, self._settings.ENDPOINT)
        await self._use_case.execute(external_existing_neighbor_identifier, endpoint)

    async def test_normal(self) -> None:
        test_neighbor_identifier = 'test-neighbor-identifier'
        endpoint = AnyUrl('http://test-neighbor:80')
        await self._use_case.execute(test_neighbor_identifier, endpoint)

        neighbor = await get_internal_neighbor(self._mock_node_repo, test_neighbor_identifier)

        self.assertEqual(neighbor.identifier, test_neighbor_identifier)
        self.assertEqual(neighbor.endpoint, endpoint)
