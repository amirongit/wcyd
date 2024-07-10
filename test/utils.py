from src.abc.service.inode_service import INodeService
from src.abc.service.ipeer_service import IPeerService
from src.service.node_service import NodeService
from src.service.peer_service import PeerService
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


def get_peer(service: IPeerService, peer_identifier: PeerIdentifier, node_identifier: NodeIdentifier) -> Peer:
    assert type(service) is PeerService, 'this is a utility to test src.service.peer_service.PeerService'
    assert type(service._peer_repo) is MockPeerRepo, 'this is a test utility'
    assert peer_identifier in service._peer_repo._mem_storage, 'peer does not exist; create it using PeerService.add first'
    obj = service._peer_repo._mem_storage[peer_identifier]
    return Peer(
        identifier=UniversalPeerIdentifier(node=node_identifier, peer=peer_identifier),
        public_key=PublicKey(
            provider=AsymmetricCryptographyProvider[obj['key_provider']],
            value=obj['key_value']
        )
    )
