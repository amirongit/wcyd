from typing import TypedDict

from redis.asyncio import Redis

from src.abc.infra.ipeer_repo import IPeerRepo
from src.settings import NodeSettings
from src.type.entity import Peer
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import Keyring, PeerIdentifier, UniversalPeerIdentifier


class RedisRepoPeerObjectModel(TypedDict):
    signing_key: str
    encryption_key: str


class PeerRepo(IPeerRepo):

    _REDIS_KEY_NAMESPACE_: str = "peer:{identifier}"

    def __init__(self, connection: Redis, node_settings: NodeSettings) -> None:
        self._connection = connection
        self._settigns = node_settings

    async def get(self, identifier: PeerIdentifier) -> Peer:
        obj: RedisRepoPeerObjectModel
        if bool(
            obj := await self._connection.hgetall(  # type: ignore
                self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)
            )  # type: ignore
        ):
            return Peer(
                identifier=UniversalPeerIdentifier(node=self._settigns.IDENTIFIER, peer=identifier),
                keyring=Keyring(
                    signing=obj["signing_key"],
                    encryption=obj["encryption_key"],
                ),
            )

        raise DoesNotExist

    async def exists(self, identifier: PeerIdentifier) -> bool:
        return (
            len(await self._connection.keys(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)))  # type: ignore
            == 1
        )

    async def create(self, identifier: PeerIdentifier, keyring: Keyring) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        obj: RedisRepoPeerObjectModel = {"signing_key": keyring.signing, "encryption_key": keyring.encryption}
        await self._connection.hmset(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier), obj)  # type: ignore

    async def delete(self, identifier: PeerIdentifier) -> None:
        if not await self.exists(identifier):
            raise DoesNotExist

        await self._connection.delete(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier))
