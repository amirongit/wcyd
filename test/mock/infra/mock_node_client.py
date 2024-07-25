from typing import TypedDict
from uuid import UUID, uuid4

from pydantic.networks import AnyUrl
from src.abc.infra.inode_client import INodeClient
from src.type.enum import AsymmetricCryptographyProvider
from src.type.internal import EndPoint, NodeIdentifier, PeerIdentifier, PublicKey, UniversalPeerIdentifier
from src.type.entity import Node, Peer
from src.type.exception import AlreadyAnswered, AlreadyExists, DoesNotExist


class MockClientNodeObjectModel(TypedDict):
    endpoint: str


class MockClientPeerObjectModel(TypedDict):
    key_provider: str
    key_value: str


class MockClientMessageObjectModel(TypedDict):
    identifier: str
    source_node: str
    source_peer: str
    content: str


class DirectNeighborMemStorage(TypedDict):
    nodes: dict[NodeIdentifier, MockClientNodeObjectModel]
    peers: dict[PeerIdentifier, MockClientPeerObjectModel]
    messages: dict[PeerIdentifier, list[MockClientMessageObjectModel]]


class MockNodeClient(INodeClient):

    def __init__(self) -> None:
        self._mem_storage: dict[NodeIdentifier, DirectNeighborMemStorage] = dict()

    async def connect_node(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        if host.identifier in self._mem_storage and identifier in self._mem_storage[host.identifier]['nodes']:
            raise AlreadyExists

        self._mem_storage[host.identifier] = {
            'nodes': {identifier: {'endpoint': str(endpoint)}},
            'peers': dict(),
            'messages': dict()
        }

    async def find_node(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        if host.identifier in questioners:
            raise AlreadyAnswered

        if (obj := self._mem_storage[host.identifier]['nodes'].get(identifier)) is None:
            raise DoesNotExist
        return Node(identifier=identifier, endpoint=AnyUrl(obj['endpoint']))

    async def find_peer(self, host: Node, identifier: UniversalPeerIdentifier) -> Peer:
        if (obj := self._mem_storage[host.identifier]['peers'].get(identifier.peer)) is None:
            raise DoesNotExist
        return Peer(
            identifier=identifier,
            public_key=PublicKey(
                provider=AsymmetricCryptographyProvider[obj['key_provider']],
                value=obj['key_value']
            )
        )

    async def send_message(
        self,
        host: Node,
        source: UniversalPeerIdentifier,
        target: UniversalPeerIdentifier,
        content: str
    ) -> None:
        if target.peer not in self._mem_storage[target.node]['peers']:
            raise DoesNotExist

        if (messages := self._mem_storage[target.node]['messages'].get(target.peer)) is None:
            self._mem_storage[target.node]['messages'][target.peer] = list()
            messages = self._mem_storage[target.node]['messages'][target.peer]

        messages.append(
            {
                'identifier': str(uuid4()),
                'source_node': source.node,
                'source_peer': source.peer,
                'content': content
            }
        )
