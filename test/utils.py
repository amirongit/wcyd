from src.abc.infra.inode_client import INodeClient
from src.abc.service.inode_service import INodeService
from src.service.node_service import NodeService
from src.type.internal import EndPoint, NodeIdentifier
from test.mock.infra.mock_node_client import MockNodeClient


def create_far_neighbor(service: INodeService, neighbor: NodeIdentifier, identifier: NodeIdentifier, endpoint: EndPoint):
    assert type(service) is NodeService, 'this is a utility to test src.service.node_service.NodeService'
    assert type(service._node_client) is MockNodeClient, 'this is a test utility'
    assert neighbor in service._node_client._mem_storage, 'neighbor does not exists; create it using NodeService.connect first'
    service._node_client._mem_storage[neighbor][identifier] = {'endpoint': str(endpoint)}
