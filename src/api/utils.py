from pydantic.networks import AnyUrl

from src.abc.infra.inode_client import INodeClient
from src.core.remote_node import RemoteNode
from src.infra.http_node_client import HTTPNodeClient
from src.infra.grpc_node_client import GRPCNodeClient
from src.type.exception import SchemaNotSupported


def remote_node_factory(identifier: str, endpoint: str, public_key: str) -> RemoteNode:

    client: INodeClient

    match AnyUrl(endpoint).scheme.lower():
        case 'http' | 'https':
            client = HTTPNodeClient()
        case 'grpc':
            client = GRPCNodeClient()
        case _:
            raise SchemaNotSupported

    return RemoteNode(identifier, public_key, endpoint, client)
