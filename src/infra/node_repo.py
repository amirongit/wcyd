from typing import TypedDict

from redis.asyncio import Redis

from src.abc.infra.inode_repo import INodeRepo
from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node
from src.type.exception import NotFound


class NodeObjectModel(TypedDict):
    endpoint: str
    public_key: str


class NodeRepo(INodeRepo):

    _REDIS_KEY_NAMESPACE_: str = 'node:{identifier}'

    def __init__(self, connection: Redis) -> None:
        self._connection = connection

    async def get(self, identifier: Identifier) -> Node:
        if bool(obj := await self._connection.hgetall(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier))): # type: ignore
            return Node(identifier=identifier, **obj) # type: ignore

        raise NotFound

    async def exists(self, identifier: Identifier) -> bool:
        return len(await self._connection.keys(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier))) == 1

    async def create(self, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None:
        obj: NodeObjectModel = {'endpoint': str(endpoint), 'public_key': public_key}
        await self._connection.hmset(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier), obj) # type: ignore

    async def all(self) -> list[Node]:
        return [
            await self.get(key.removeprefix('node:')) for key in await self._connection.keys(
                self._REDIS_KEY_NAMESPACE_.format(identifier='*')
            )
        ]
