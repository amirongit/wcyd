from pydantic import AnyUrl
from src.type.entity import Node, Peer
from src.type.enum import AsymmetricCryptographyProvider
from src.type.internal import EndPoint, NodeIdentifier, PeerIdentifier, PublicKey, UniversalPeerIdentifier
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.mock.infra.mock_peer_repo import MockPeerRepo


def add_far_neighbor(
    node_client: MockNodeClient,
    direct_neighbor: NodeIdentifier,
    far_neighbor: NodeIdentifier,
    endpoint: EndPoint
) -> None:
    '''WARNING: this function resets a key in the _mem_storage dictionary; read the code before using'''

    node_client._mem_storage[direct_neighbor] = {far_neighbor: {'endpoint': str(endpoint)}}


def get_peer(peer_repo: MockPeerRepo, peer_identifier: PeerIdentifier, node_identifier: NodeIdentifier) -> Peer:
    assert peer_identifier in peer_repo._mem_storage, 'peer does not exist'

    obj = peer_repo._mem_storage[peer_identifier]
    return Peer(
        identifier=UniversalPeerIdentifier(node=node_identifier, peer=peer_identifier),
        public_key=PublicKey(
            provider=AsymmetricCryptographyProvider[obj['key_provider']],
            value=obj['key_value']
        )
    )


def add_peer(peer_repo: MockPeerRepo, peer_identifier: PeerIdentifier, public_key: PublicKey) -> None:
    assert peer_identifier not in peer_repo._mem_storage, 'peer already exists'

    peer_repo._mem_storage[peer_identifier] = {'key_provider': public_key.provider.name, 'key_value': public_key.value}


def get_node(node_repo: MockNodeRepo, identifier: NodeIdentifier) -> Node:
    assert identifier in node_repo._mem_storage, 'node does not exist'

    return Node(identifier=identifier, endpoint=AnyUrl(node_repo._mem_storage[identifier]['endpoint']))


def add_node(node_repo: MockNodeRepo, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
    assert identifier not in node_repo._mem_storage, 'node already exists'

    node_repo._mem_storage[identifier] = {'endpoint': str(endpoint)}
