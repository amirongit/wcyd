from typing import TypedDict
from uuid import UUID, uuid4

from redis.asyncio import Redis

from src.abc.infra.imessage_repo import IMessageRepo
from src.settings import NodeSettings
from src.type.entity import Message
from src.type.internal import PeerIdentifier, UniversalPeerIdentifier


class RedisRepoMessageObjectModel(TypedDict):
    source_node: str
    source_peer: str
    content: str


class MessageRepo(IMessageRepo):

    _REDIS_KEY_NAMESPACE_: str = "message:{identifier}:{target_identifier}"

    def __init__(self, connection: Redis, node_settings: NodeSettings) -> None:
        self._connection = connection
        self._settigns = node_settings

    async def create(self, source: UniversalPeerIdentifier, target: PeerIdentifier, content: str) -> None:
        obj: RedisRepoMessageObjectModel = {"source_node": source.node, "source_peer": source.peer, "content": content}
        await self._connection.hmset(
            self._REDIS_KEY_NAMESPACE_.format(identifier=uuid4(), target_identifier=target), obj  # type: ignore
        )

    async def relative_to_target(self, identifier: PeerIdentifier) -> list[Message]:
        message_list: list[Message] = []

        for key in await self._connection.keys(
            self._REDIS_KEY_NAMESPACE_.format(identifier="*", target_identifier=identifier)
        ):
            obj: RedisRepoMessageObjectModel = await self._connection.hgetall(key)  # type: ignore
            Message(
                identifier=UUID(key.split(":")[1]),
                source=UniversalPeerIdentifier(node=obj["source_peer"], peer=obj["source_peer"]),
                target=UniversalPeerIdentifier(node=self._settigns.IDENTIFIER, peer=identifier),
                content=obj["content"],
            )

        return message_list
