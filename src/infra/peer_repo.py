from typing import TypedDict

from redis.asyncio import Redis

from src.abc.infra.ipeer_repo import IPeerRepo
from src.settings import NodeSettings
from src.type.entity import Peer
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import PeerIdentifier, PublicKey, UniversalPeerIdentifier


class RedisRepoPeerObjectModel(TypedDict):
    key_provider: str
    key_value: str


class PeerRepo(IPeerRepo):

    _REDIS_KEY_NAMESPACE_: str = 'peer:{identifier}'

    def __init__(self, connection: Redis, node_settings: NodeSettings) -> None:
        self._connection = connection
        self._settigns = node_settings

    async def get(self, identifier: PeerIdentifier) -> Peer:
        obj: RedisRepoPeerObjectModel
        if bool(
            obj := await self._connection.hgetall(
                self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)
            ) # type: ignore
        ):
            return Peer(
                identifier=UniversalPeerIdentifier(node=self._settigns.IDENTIFIER, peer=identifier),
                public_key=PublicKey(
                    provider=AsymmetricCryptographyProvider[obj['key_provider']],
                    value=obj['key_value']
                )
            )

        raise DoesNotExist

    async def exists(self, identifier: PeerIdentifier) -> bool:
        return len(await self._connection.keys(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier))) == 1

    async def create(self, identifier: PeerIdentifier, public_key: PublicKey) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        obj: RedisRepoPeerObjectModel = {'key_provider': public_key.provider.name, 'key_value': public_key.value}
        await self._connection.hmset(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier), obj) # type: ignore

    async def delete(self, identifier: PeerIdentifier) -> None:
        if not await self.exists(identifier):
            raise DoesNotExist

        await self._connection.delete(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)) 
