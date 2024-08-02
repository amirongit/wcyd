from blacksheep import FromJSON, FromRoute, Request, Response
from blacksheep.server.controllers import post
from guardpost import Identity

from src.abc.use_case.send_message_use_case import SendMessageUseCase
from src.api.controller.base_controller import BaseController
from src.api.docs import docs
from src.api.io_type.message_io import MessageTransferRequest
from src.type.internal import UniversalPeerIdentifier


class RelatedMessageController(BaseController):

    ROUTE = '/nodes/{node_identifier}/peers/{peer_identifier}/messages'

    def __init__(self, send_message_use_case: SendMessageUseCase,) -> None:
        self._send_use_case = send_message_use_case

    @docs(
        tags=['messages'],
        summary='leave the provided message for the target peer',
        responses={201: 'message left successfully', 404: 'not found'}
    )
    @post('/')
    async def leave_message(
        self,
        identity: Identity,
        node_identifier: FromRoute[str],
        peer_identifier: FromRoute[str],
        request_body: FromJSON[MessageTransferRequest],
        request: Request
    ) -> Response:
        source: UniversalPeerIdentifier = identity['id']
        credentials: PeerCredentials = request.get_first_header(b'Authorization').decode() # type: ignore

        await self._send_use_case.execute(
            source,
            UniversalPeerIdentifier(node=node_identifier.value, peer=peer_identifier.value),
            request_body.value.content,
            credentials
        )

        return self.created()
