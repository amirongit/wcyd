from uuid import UUID
from src.type.entity import Message, Node, Peer
from src.type.internal import EndPoint, NodeIdentifier, PeerIdentifier, PublicKey, UniversalPeerIdentifier
from test.mock.infra.mock_message_repo import MockMessageRepo
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.mock.infra.mock_peer_repo import MockPeerRepo


def add_external_neighbor(
    client: MockNodeClient,
    direct_neighbor: NodeIdentifier,
    far_neighbor: NodeIdentifier,
    endpoint: EndPoint
) -> None:
    if direct_neighbor in client._mem_storage:
        client._mem_storage[direct_neighbor]['nodes'].update({far_neighbor: {'endpoint': str(endpoint)}})
    else:
        client._mem_storage[direct_neighbor] = {
            'nodes': {far_neighbor: {'endpoint': str(endpoint)}},
            'peers': dict(),
            'messages': dict()
        }


def add_external_peer(
    client: MockNodeClient,
    direct_neighbor: NodeIdentifier,
    peer: PeerIdentifier,
    public_key: PublicKey
) -> None:
    if direct_neighbor in client._mem_storage:
        client._mem_storage[direct_neighbor]['peers'].update(
            {peer: {'key_provider': public_key.provider.name, 'key_value': public_key.value}}
        )
    else:
        client._mem_storage[direct_neighbor] = {
            'peers': {peer: {'key_provider': public_key.provider.name, 'key_value': public_key.value}},
            'nodes': dict(),
            'messages': dict()
        }


async def get_internal_peer(repo: MockPeerRepo, peer_identifier: PeerIdentifier) -> Peer:
    assert peer_identifier in repo._mem_storage, 'peer does not exist'

    return await repo.get(peer_identifier)


def add_internal_peer(repo: MockPeerRepo, peer_identifier: PeerIdentifier, public_key: PublicKey) -> None:
    assert peer_identifier not in repo._mem_storage, 'peer already exists'

    repo._mem_storage[peer_identifier] = {'key_provider': public_key.provider.name, 'key_value': public_key.value}


async def get_internal_neighbor(repo: MockNodeRepo, identifier: NodeIdentifier) -> Node:
    assert identifier in repo._mem_storage, 'node does not exist'

    return await repo.get(identifier)


def add_internal_neighbor(repo: MockNodeRepo, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
    assert identifier not in repo._mem_storage, 'node already exists'

    repo._mem_storage[identifier] = {'endpoint': str(endpoint)}


async def get_internal_relative_messages(repo: MockMessageRepo, identifier: PeerIdentifier) -> list[Message]:
    assert identifier in repo._mem_storage, 'peer does not exist'

    return await repo.relative_to_target(identifier)


def get_external_relative_messages(client: MockNodeClient, identifier: UniversalPeerIdentifier) -> list[Message]:
    assert identifier.node in client._mem_storage, 'node does not exist'
    assert identifier.peer in client._mem_storage[identifier.node]['peers'], 'peer does not exist'

    try:
        return [
            Message(
                identifier=UUID(obj['identifier']),
                source=UniversalPeerIdentifier(node=obj['source_node'], peer=obj['source_peer']),
                target=identifier,
                content=obj['content']
            ) for obj in client._mem_storage[identifier.node]['messages'][identifier.peer]
        ]
    except KeyError:
        return list()
