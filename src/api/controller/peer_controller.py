from blacksheep import FromJSON, Response
from blacksheep.server.authorization import allow_anonymous
from blacksheep.server.controllers import post

from src.abc.use_case.add_peer_use_case import AddPeerUseCase
from src.api.docs import docs, unsecure_handler
from src.api.controller.base_controller import BaseController
from src.api.io_type.peer_io import PeerCreationRequest


class PeerController(BaseController):

    ROUTE = '/peers'

    def __init__(self, add_use_case: AddPeerUseCase) -> None:
        self._add_use_case = add_use_case

    @docs(
        tags=['peers'],
        summary='register provided peer in node',
        responses={201: 'registeration done successfully', 409: 'duplicated identifier'},
        on_created=unsecure_handler
    )
    @allow_anonymous()
    @post('/')
    async def register_peer(self, request_body: FromJSON[PeerCreationRequest]) -> Response:

        await self._add_use_case.execute(request_body.value.identifier, request_body.value.keyring)

        return self.created()
