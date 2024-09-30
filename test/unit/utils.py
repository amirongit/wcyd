from base64 import b64encode
from test.unit.mock.infra.mock_message_repo import MockMessageRepo
from test.unit.mock.infra.mock_node_client import MockNodeClient
from test.unit.mock.infra.mock_node_repo import MockNodeRepo
from test.unit.mock.infra.mock_peer_repo import MockPeerRepo
from uuid import UUID, uuid4

from src.type.entity import Message, Node, Peer
from src.type.internal import EndPoint, Keyring, NodeIdentifier, PeerIdentifier, UniversalPeerIdentifier


def make_auth_credentials(identifier: UniversalPeerIdentifier) -> str:
    return b64encode(bytes(f"Basic {identifier.peer}@{identifier.node}:cant-be-tested".encode())).decode()


# pylint: disable=protected-access
def add_external_neighbor(
    client: MockNodeClient, direct_neighbor: NodeIdentifier, far_neighbor: NodeIdentifier, endpoint: EndPoint
) -> None:
    if direct_neighbor in client._mem_storage:
        client._mem_storage[direct_neighbor]["nodes"].update({far_neighbor: {"endpoint": str(endpoint)}})
    else:
        client._mem_storage[direct_neighbor] = {
            "nodes": {far_neighbor: {"endpoint": str(endpoint)}},
            "peers": {},
            "messages": {},
        }


# pylint: disable=protected-access
def add_external_peer(
    client: MockNodeClient, direct_neighbor: NodeIdentifier, peer: PeerIdentifier, keyring: Keyring
) -> None:
    if direct_neighbor in client._mem_storage:
        client._mem_storage[direct_neighbor]["peers"].update(
            {peer: {"signing_key": keyring.signing, "encryption_key": keyring.encryption}}
        )
    else:
        client._mem_storage[direct_neighbor] = {
            "peers": {peer: {"signing_key": keyring.signing, "encryption_key": keyring.encryption}},
            "nodes": {},
            "messages": {},
        }


# pylint: disable=protected-access
async def get_internal_peer(repo: MockPeerRepo, peer_identifier: PeerIdentifier) -> Peer:
    assert peer_identifier in repo._mem_storage, "peer does not exist"

    return await repo.get(peer_identifier)


# pylint: disable=protected-access
def add_internal_peer(repo: MockPeerRepo, peer_identifier: PeerIdentifier, public_key: Keyring) -> None:
    assert peer_identifier not in repo._mem_storage, "peer already exists"

    repo._mem_storage[peer_identifier] = {"signing_key": public_key.signing, "encryption_key": public_key.encryption}


# pylint: disable=protected-access
async def get_internal_neighbor(repo: MockNodeRepo, identifier: NodeIdentifier) -> Node:
    assert identifier in repo._mem_storage, "node does not exist"

    return await repo.get(identifier)


# pylint: disable=protected-access
def add_internal_neighbor(repo: MockNodeRepo, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
    assert identifier not in repo._mem_storage, "node already exists"

    repo._mem_storage[identifier] = {"endpoint": str(endpoint)}


# pylint: disable=protected-access
async def get_internal_relative_messages(repo: MockMessageRepo, identifier: PeerIdentifier) -> list[Message]:
    assert identifier in repo._mem_storage, "peer does not exist"

    return await repo.relative_to_target(identifier)


# pylint: disable=protected-access
def get_external_relative_messages(client: MockNodeClient, identifier: UniversalPeerIdentifier) -> list[Message]:
    assert identifier.node in client._mem_storage, "node does not exist"
    assert identifier.peer in client._mem_storage[identifier.node]["peers"], "peer does not exist"

    try:
        return [
            Message(
                identifier=UUID(obj["identifier"]),
                source=UniversalPeerIdentifier(node=obj["source_node"], peer=obj["source_peer"]),
                target=identifier,
                content=obj["content"],
            )
            for obj in client._mem_storage[identifier.node]["messages"][identifier.peer]
        ]
    except KeyError:
        return []


async def add_internal_message(
    repo: MockMessageRepo, source: UniversalPeerIdentifier, target: PeerIdentifier, content: str
) -> None:
    await repo.create(source, target, content)


# pylint: disable=protected-access
def add_external_message(
    client: MockNodeClient, source: UniversalPeerIdentifier, target: UniversalPeerIdentifier, content: str
) -> None:
    assert target.node in client._mem_storage, "node does not exist"
    assert target.peer in client._mem_storage[target.node]["peers"], "peer does not exist"

    if (messages := client._mem_storage[target.node]["messages"].get(target.peer)) is None:
        client._mem_storage[target.node]["messages"][target.peer] = []
        messages = client._mem_storage[target.node]["messages"][target.peer]

    messages.append(
        {"identifier": str(uuid4()), "source_node": source.node, "source_peer": source.peer, "content": content}
    )
