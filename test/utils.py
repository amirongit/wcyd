from src.abc.service.inode_service import INodeService
from src.service.node_service import NodeService
from src.type.entity import Peer
from src.type.enum import AsymmetricCryptographyProvider
from src.type.internal import EndPoint, NodeIdentifier, PeerIdentifier, PublicKey, UniversalPeerIdentifier
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_peer_repo import MockPeerRepo


def create_far_neighbor(service: INodeService, neighbor: NodeIdentifier, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
    assert type(service) is NodeService, 'this is a utility to test src.service.node_service.NodeService'
    assert type(service._node_client) is MockNodeClient, 'this is a test utility'
    assert neighbor in service._node_client._mem_storage, 'neighbor does not exist; create it using NodeService.connect first'

    service._node_client._mem_storage[neighbor][identifier] = {'endpoint': str(endpoint)}


def get_peer(peer_repo: MockPeerRepo, peer_identifier: PeerIdentifier, node_identifier: NodeIdentifier) -> Peer:
    assert peer_identifier in peer_repo._mem_storage, 'peer does not exist; create it using PeerService.add first'

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
