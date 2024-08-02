from blacksheep import Request, Response
from blacksheep.server.controllers import get
from blacksheep.server.openapi.common import ContentInfo, ResponseInfo
from guardpost import Identity

from src.abc.use_case.get_related_messages_use_case import GetRelatedMessagesUseCase
from src.api.controller.base_controller import BaseController
from src.api.docs import docs
from src.api.io_type.message_io import MessageModel
from src.type.internal import PeerCredentials, UniversalPeerIdentifier


class MessageController(BaseController):

    ROUTE = '/messages'

    def __init__(self, get_related_messages_use_case: GetRelatedMessagesUseCase) -> None:
        self._get_use_case = get_related_messages_use_case

    @docs(
        tags=['messages'],
        summary='get messages related to the authenticated peer',
        responses={200: ResponseInfo('information of the queried node', content=[ContentInfo(list[MessageModel])])}
    )
    @get('/')
    async def get_related_messages(self, identity: Identity, request: Request) -> Response:
        target: UniversalPeerIdentifier = identity['id']

        header_value: bytes = request.get_first_header(b'Authorization') # type: ignore
        credentials: PeerCredentials = header_value.decode()

        return self.ok(
            MessageModel(
                identifier=m.identifier,
                source=m.source,
                content=m.content
            ) for m in await self._get_use_case.execute(target, credentials)
        )
