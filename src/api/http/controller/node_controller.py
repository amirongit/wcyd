from blacksheep.server.controllers import post
from blacksheep import FromJSON, Response

from src.core.local_node import LocalNode
from src.core.remote_node import RemoteNode
from src.api.http.controller.base_controller import BaseController
from src.api.http.io_type.node_io import NodeConnectionRequest
from src.api.utils import remote_node_factory


class NodeController(BaseController):

    ROUTE = '/nodes'

    def __init__(self, local_node: LocalNode) -> None:
        self._local_node = local_node

    @post('/')
    async def connect(self, request_body: FromJSON[NodeConnectionRequest]) -> Response:

        serialized = request_body.value
        remote_node: RemoteNode = remote_node_factory(
            serialized.identifier,
            serialized.endpoint,
            serialized.public_key
        )
        await self._local_node.connect(remote_node)

        return self.created()
