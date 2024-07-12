from blacksheep import FromJSON, FromRoute, Response
from blacksheep.server.controllers import post, get
from blacksheep.server.openapi.common import ContentInfo, ResponseInfo

from src.abc.use_case.add_peer_use_case import AddPeerUseCase
from src.abc.use_case.find_peer_use_case import FindPeerUseCase
from src.api.docs import docs
from src.api.controller.base_controller import BaseController
from src.api.io_type.peer_io import PeerCreationRequest, PeerModel
from src.type.internal import UniversalPeerIdentifier


class PeerController(BaseController):

    ROUTE = '/peers'

    def __init__(self, add_use_case: AddPeerUseCase, find_use_case: FindPeerUseCase) -> None:
        self._add_use_case = add_use_case
        self._find_peer_use_case = find_use_case

    @docs(
        tags=['peers'],
        summary='register provided peer in node',
        responses={201: 'registeration done successfully', 409: 'duplicated identifier'}
    )
    @post('/')
    async def register_peer(self, request_body: FromJSON[PeerCreationRequest]) -> Response:

        await self._add_use_case.execute(request_body.value.identifier, request_body.value.public_key)

        return self.created()

    @docs(
        tags=['peers'],
        summary='get information of a peer within the network which this node is a part of',
        responses={
            200: ResponseInfo('information of the queried peer', content=[ContentInfo(PeerModel)]),
            404: 'not found',
        }
    )
    @get('/{node_identifier}/{peer_identifier}')
    async def get_peer(self, node_identifier: FromRoute[str], peer_identifier: FromRoute[str]) -> Response:

        peer = await self._find_peer_use_case.execute(
            UniversalPeerIdentifier(node=node_identifier.value, peer=peer_identifier.value)
        )

        return self.ok(PeerModel(identifier=peer.identifier, public_key=peer.public_key))
