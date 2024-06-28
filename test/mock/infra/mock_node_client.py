from typing import TypedDict

from pydantic.networks import AnyUrl
from src.abc.infra.inode_client import INodeClient
from src.type.internal import EndPoint, NodeIdentifier
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound


class MockClientNodeObjectModel(TypedDict):
    endpoint: str


class MockNodeClient(INodeClient):

    def __init__(self) -> None:
        self._mem_storage: dict[NodeIdentifier, dict[NodeIdentifier, MockClientNodeObjectModel]] = dict()

    async def get_neighbors(self, host: Node) -> list[Node]:
        try:
            return [
                Node(
                    identifier=k,
                    endpoint=AnyUrl(v['endpoint']),
                ) for k, v in self._mem_storage[host.identifier].items()
            ]
        except KeyError as e:
            raise Exception from e

    async def connect(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        if host.identifier in self._mem_storage:
            raise AlreadyExists

        self._mem_storage[host.identifier] = dict()

    async def find(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        if host.identifier in questioners:
            raise AlreadyAnswered

        try:
            if (obj := self._mem_storage[host.identifier].get(identifier)) is None:
                raise NotFound
            return Node(identifier=identifier, endpoint=AnyUrl(obj['endpoint']))
        except KeyError as e:
            raise Exception from e

