from typing import TypedDict

from redis.asyncio import Redis

from src.abc.infra.inode_repo import INodeRepo
from src.type.entity import Node
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import EndPoint, NodeIdentifier


class RedisRepoNodeObjectModel(TypedDict):
    endpoint: str


class NodeRepo(INodeRepo):

    _REDIS_KEY_NAMESPACE_: str = "node:{identifier}"

    def __init__(self, connection: Redis) -> None:
        self._connection = connection

    async def get(self, identifier: NodeIdentifier) -> Node:
        if bool(
            obj := await self._connection.hgetall(  # type: ignore
                self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)
            )
        ):
            return Node(identifier=identifier, **obj)  # type: ignore

        raise DoesNotExist

    async def exists(self, identifier: NodeIdentifier) -> bool:
        return (
            len(await self._connection.keys(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier)))  # type: ignore
            == 1
        )

    async def create(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        obj: RedisRepoNodeObjectModel = {"endpoint": str(endpoint)}
        await self._connection.hmset(self._REDIS_KEY_NAMESPACE_.format(identifier=identifier), obj)  # type: ignore

    async def all(self) -> list[Node]:
        return [
            await self.get(key.removeprefix("node:"))
            for key in await self._connection.keys(self._REDIS_KEY_NAMESPACE_.format(identifier="*"))  # type: ignore
        ]
