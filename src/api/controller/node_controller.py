from blacksheep import FromJSON, FromRoute, FromQuery, Response
from blacksheep.server.controllers import post, get
from blacksheep.server.openapi.common import ContentInfo, ResponseInfo

from src.abc.use_case.connect_node_use_case import ConnectNodeUseCase
from src.abc.use_case.find_node_use_case import FindNodeUseCase
from src.api.controller.base_controller import BaseController
from src.api.docs import docs
from src.api.io_type.node_io import NodeConnectionRequest, NodeModel


class NodeController(BaseController):

    ROUTE = '/nodes'

    def __init__(self, connect_use_case: ConnectNodeUseCase, find_node_use_case: FindNodeUseCase) -> None:
        self._connect_use_case = connect_use_case
        self._find_use_case = find_node_use_case

    @docs(
        tags=['nodes'],
        summary='register provided node as neighbor',
        responses={201: 'registeration done successfully', 409: 'already connected'}
    )
    @post('/')
    async def register_node(self, request_body: FromJSON[NodeConnectionRequest]) -> Response:

        serialized = request_body.value
        await self._connect_use_case.execute(serialized.identifier, serialized.endpoint)

        return self.created()

    @docs(
        tags=['nodes'],
        summary='get information of a node within the network which this node is a part of',
        responses={
            200: ResponseInfo('information of the queried node', content=[ContentInfo(NodeModel)]),
            404: 'not found',
            409: 'already answered'
        }
    )
    @get('/{identifier}')
    async def get_node(self, identifier: FromRoute[str], questioners: FromQuery[set[str]]) -> Response:

        node = await self._find_use_case.execute(questioners.value, identifier.value)

        return self.ok(NodeModel(identifier=node.identifier, endpoint=str(node.endpoint)))
