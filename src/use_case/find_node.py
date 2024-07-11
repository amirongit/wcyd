from src.abc.infra.inode_client import INodeClient
from src.abc.infra.inode_repo import INodeRepo
from src.abc.use_case.find_node_use_case import FindNodeUseCase
from src.settings import NodeSettings
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, DoesNotExist
from src.type.internal import NodeIdentifier


class FindNode(FindNodeUseCase):
    def __init__(self, node_settings: NodeSettings, node_repo: INodeRepo, node_client: INodeClient) -> None:
        self._settings = node_settings
        self._node_repo = node_repo
        self._node_client = node_client

    async def execute(self, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        if self._settings.IDENTIFIER in questioners:
            raise AlreadyAnswered

        try:
            return await self._node_repo.get(identifier)
        except DoesNotExist:
            new_questioners = questioners | {self._settings.IDENTIFIER}
            for node in filter(lambda n: n.identifier not in new_questioners, await self._node_repo.all()):
                try:
                    return await self._node_client.find(node, new_questioners, identifier)
                except DoesNotExist:
                    new_questioners.add(node.identifier)
                except AlreadyAnswered:
                    continue

        raise DoesNotExist
