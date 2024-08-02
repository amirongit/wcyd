from typing import TypedDict
from uuid import uuid4, UUID

from pydantic.networks import AnyUrl

from src.abc.infra.inode_client import INodeClient
from src.type.internal import EndPoint, NodeIdentifier, PeerCredentials, PeerIdentifier, Keyring, UniversalPeerIdentifier
from src.type.entity import Node, Peer, Message
from src.type.exception import AlreadyAnswered, AlreadyExists, DoesNotExist


class MockClientNodeObjectModel(TypedDict):
    endpoint: str


class MockClientPeerObjectModel(TypedDict):
    signing_key: str
    encryption_key: str


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
            keyring=Keyring(
                signing=obj['signing_key'],
                encryption=obj['encryption_key']
            )
        )

    async def send_message(
        self,
        host: Node,
        credentials: PeerCredentials,
        target: UniversalPeerIdentifier,
        content: str
    ) -> None:
        if target.peer not in self._mem_storage[target.node]['peers']:
            raise DoesNotExist

        if (messages := self._mem_storage[target.node]['messages'].get(target.peer)) is None:
            self._mem_storage[target.node]['messages'][target.peer] = list()
            messages = self._mem_storage[target.node]['messages'][target.peer]

        source = self._authenticated_credentials(credentials)
        messages.append(
            {
                'identifier': str(uuid4()),
                'source_node': source.node,
                'source_peer': source.peer,
                'content': content
            }
        )

    async def get_related_messages(
        self,
        host: Node,
        target: UniversalPeerIdentifier,
        credentials: PeerCredentials
    ) -> list[Message]:
        if target.peer not in self._mem_storage[target.node]['peers']:
            raise DoesNotExist

        if (messages := self._mem_storage[target.node]['messages'].get(target.peer)) is None:
            return list()

        return [
            Message(
                identifier=UUID(obj['identifier']),
                source=UniversalPeerIdentifier(peer=obj['source_peer'], node=obj['source_node']),
                target=target,
                content=obj['content']
            ) for obj in messages
        ]

    @staticmethod
    def _authenticated_credentials(credentials: PeerCredentials) -> UniversalPeerIdentifier:
        peer_identifier, node_identifier = credentials.removeprefix('Basic ').split(':')[0].split('@')
        return UniversalPeerIdentifier(peer=peer_identifier, node=node_identifier)
