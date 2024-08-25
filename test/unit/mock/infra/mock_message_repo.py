from typing import TypedDict
from uuid import UUID, uuid4

from src.abc.infra.imessage_repo import IMessageRepo
from src.settings import NodeSettings
from src.type.entity import Message
from src.type.internal import PeerIdentifier, UniversalPeerIdentifier


class MockRepoMessageObjectModel(TypedDict):
    identifier: UUID
    source_node: str
    source_peer: str
    content: str


class MockMessageRepo(IMessageRepo):
    def __init__(self, node_settings: NodeSettings) -> None:
        self._mem_storage: dict[PeerIdentifier, list[MockRepoMessageObjectModel]] = {}
        self._settings = node_settings

    async def create(self, source: UniversalPeerIdentifier, target: PeerIdentifier, content: str) -> None:
        try:
            messages = self._mem_storage[target]
        except KeyError:
            self._mem_storage[target] = []
            messages = self._mem_storage[target]

        messages.append(
            {
                'identifier': uuid4(),
                'source_node': source.node,
                'source_peer': source.peer,
                'content': content
            }
        )

    async def relative_to_target(self, identifier: PeerIdentifier) -> list[Message]:
        try:
            return [
                Message(
                    identifier=obj['identifier'],
                    source=UniversalPeerIdentifier(node=obj['source_node'], peer=obj['source_peer']),
                    target=UniversalPeerIdentifier(node=self._settings.IDENTIFIER, peer=identifier),
                    content=obj['content']
                ) for obj in self._mem_storage[identifier]
            ]
        except KeyError:
            return []
