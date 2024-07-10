from blacksheep import FromJSON, Response
from blacksheep.server.controllers import post

from src.abc.service.ipeer_service import IPeerService
from src.api.docs import docs
from src.api.controller.base_controller import BaseController
from src.api.io_type.peer_io import PeerCreationRequest


class PeerController(BaseController):

    ROUTE = '/peers'

    def __init__(self, peer_service: IPeerService):
        self._peer_service = peer_service

    @docs(
        tags=['peers'],
        summary='register provided peer in node',
        responses={201: 'registeration done successfully', 409: 'duplicated identifier'}
    )
    @post('/')
    async def register_peer(self, request_body: FromJSON[PeerCreationRequest]) -> Response:

        serialized = request_body.value
        await self._peer_service.add(serialized.identifier, serialized.public_key)

        return self.created()
