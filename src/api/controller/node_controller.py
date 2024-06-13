from blacksheep.server.controllers import post
from blacksheep import FromJSON, Response

from src.abc.service.inode_service import INodeService
from src.api.controller.base_controller import BaseController
from src.api.io_type.node_io import NodeConnectionRequest


class NodeController(BaseController):

    ROUTE = '/nodes'

    def __init__(self, node_service: INodeService) -> None:
        self._node_service = node_service

    @post('/')
    async def connect(self, request_body: FromJSON[NodeConnectionRequest]) -> Response:

        serialized = request_body.value
        await self._node_service.connect(serialized.identifier, serialized.endpoint, serialized.public_key)

        return self.created()
