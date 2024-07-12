from typing import TypedDict

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


class DirectNeighborMemStorage(TypedDict):
    nodes: dict[NodeIdentifier, MockClientNodeObjectModel]
    peers: dict[PeerIdentifier, MockClientPeerObjectModel]


class MockNodeClient(INodeClient):

    def __init__(self) -> None:
        self._mem_storage: dict[NodeIdentifier, DirectNeighborMemStorage] = dict()

    async def connect_node(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        if host.identifier in self._mem_storage:
            raise AlreadyExists

        self._mem_storage[host.identifier] = {'nodes': {identifier: {'endpoint': str(endpoint)}}, 'peers': dict()}

    async def find_node(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        if host.identifier in questioners:
            raise AlreadyAnswered

        try:
            if (obj := self._mem_storage[host.identifier]['nodes'].get(identifier)) is None:
                raise DoesNotExist
            return Node(identifier=identifier, endpoint=AnyUrl(obj['endpoint']))
        except KeyError as e:
            raise Exception from e

    async def find_peer(self, host: Node, identifier: UniversalPeerIdentifier) -> Peer:
        try:
            if (obj := self._mem_storage[host.identifier]['peers'].get(identifier.peer)) is None:
                raise DoesNotExist
            return Peer(
                identifier=identifier,
                public_key=PublicKey(
                    provider=AsymmetricCryptographyProvider[obj['key_provider']],
                    value=obj['key_value']
                )
            )
        except KeyError as e:
            raise Exception from e
