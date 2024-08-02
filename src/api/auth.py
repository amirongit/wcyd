from datetime import datetime, timedelta

from blacksheep import Application, Request
from guardpost import AuthenticationHandler, Identity

from src.abc.use_case.find_peer_use_case import FindPeerUseCase
from src.settings import AuthenticationSettings
from src.type.internal import UniversalPeerIdentifier
from src.utils import EncryptionUtils


class DecentralizedAuthenticationHandler(AuthenticationHandler):

    '''
    authentication steps:
        a. the peer (client) signs a timestamp with its private signing key
        b. the signed timestamp is placed in the `Authorization` header with an specific format *
        c. the node (server) acquires the peer's public signing key and verifies the signed timestamp
        d. if the timestamp is within the range of +/- `settings.AUTHENTICATION.TOKEN_TIME_WINDOW`,
           the peer is authenticated within the scope of the request

    * header format: Basic Base64.encode(peer@node:hex(signed_timestamp))
    '''

    def __init__(self, app: Application) -> None:
        super().__init__()
        self.app = app

    @property
    def _find_peer_use_case(self) -> FindPeerUseCase: return self.app.services.resolve(FindPeerUseCase)

    @property
    def _settings(self) -> AuthenticationSettings: return self.app.services.resolve(AuthenticationSettings)

    async def authenticate(self, context: Request) -> Identity | None: # type: ignore
        context.identity = None

        try:
            identifier, signature = EncryptionUtils.decrypt_base64(
                context.get_first_header(b'Authorization').decode().removeprefix('Basic ') # type: ignore
            ).split(':')
            peer_identifier, node_identifier = identifier.split('@')
            universal_identifier = UniversalPeerIdentifier(peer=peer_identifier, node=node_identifier)
            peer = await self._find_peer_use_case.execute(universal_identifier)
            signed_timestamp  = float(EncryptionUtils.verify_signature(signature, peer.keyring.signing))
            now, window_range = datetime.now(), timedelta(seconds=self._settings.TIME_WINDOW)
            start, end = now - window_range, now + window_range
            given = datetime.fromtimestamp(signed_timestamp)
            if given > start and given < end:
                context.identity = Identity({'id': universal_identifier}, 'authenticated')
        except Exception:
            pass

        return context.identity
