from datetime import datetime, timedelta

from blacksheep import Request
from guardpost import AuthenticationHandler, Identity

from src.settings import AuthenticationSettings
from src.type.internal import UniversalPeerIdentifier
from src.use_case.find_peer import FindPeerUseCase
from src.utils import EncryptionUtils


class DecentralizedAuthenticationHandler(AuthenticationHandler):

    '''
    authentication steps:
        a. the peer (client) signs a timestamp with its private signing key
        b. the signed timestamp is placed in the `Authorization` header with an specific format *
        c. the node (server) acquires the peer's public signing key and verifies the signed timestamp
        d. if the timestamp is within the range of +/- `settings.AUTHENTICATION.TOKEN_TIME_WINDOW`,
           the peer is authenticated within the scope of the request

    * Authorization header format: Basic Base64.encode(peer@node:signed_timestamp)
    '''

    def __init__(self, find_peer_use_case: FindPeerUseCase, node_settings: AuthenticationSettings) -> None:
        self._find_peer_use_case = find_peer_use_case
        self._settings = node_settings

    async def authenticate(self, context: Request) -> Identity | None: # type: ignore
        context.identity = None

        try:
            identifier, signature = EncryptionUtils.decrypt_base64(
                    context.headers.get(b'Authorization')[0][1].decode().removeprefix('Basic ')
            ).split(':')
            peer_identifier, node_identifier = identifier.split('@')
            universal_identifier = UniversalPeerIdentifier(peer=peer_identifier, node=node_identifier)
            peer = await self._find_peer_use_case.execute(universal_identifier)
            content  = EncryptionUtils.verify_signature(signature, peer.keyring.signing)
            now, window_range = datetime.now(), timedelta(seconds=self._settings.TIME_WINDOW)
            start, end = now - window_range, now + window_range
            given = datetime.fromtimestamp(int(content)) # type: ignore
            if given > start and given < end:
                context.identity = Identity({'id': universal_identifier})
        except Exception:
            pass

        return context.identity
