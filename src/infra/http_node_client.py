from src.abc.core.inode import INode
from src.abc.infra.inode_client import INodeClient
from src.type.dto import ChannelDTO
from src.type.alias import Identifier

class HTTPNodeClient(INodeClient):

    async def get_neighbors(self, channel: ChannelDTO) -> set[Identifier]:
        raise NotImplemented

    async def connect_node(self, channel: ChannelDTO) -> None:
        raise NotImplemented

    async def find_node(self, questioners: set[Identifier], identifier: Identifier) -> INode:
        raise NotImplemented
