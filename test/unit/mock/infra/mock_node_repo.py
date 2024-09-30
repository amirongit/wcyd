from typing import TypedDict

from pydantic.networks import AnyUrl

from src.abc.infra.inode_repo import INodeRepo
from src.type.entity import Node
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import EndPoint, NodeIdentifier


class MockRepoNodeObjectModel(TypedDict):
    endpoint: str


class MockNodeRepo(INodeRepo):

    def __init__(self) -> None:
        self._mem_storage: dict[NodeIdentifier, MockRepoNodeObjectModel] = {}

    async def get(self, identifier: NodeIdentifier) -> Node:
        if (obj := self._mem_storage.get(identifier)) is not None:
            return Node(identifier=identifier, **obj)  # type: ignore

        raise DoesNotExist

    async def exists(self, identifier: NodeIdentifier) -> bool:
        return identifier in self._mem_storage

    async def create(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        self._mem_storage[identifier] = {"endpoint": str(endpoint)}

    async def all(self) -> list[Node]:
        return [
            Node(
                identifier=k,
                endpoint=AnyUrl(v["endpoint"]),
            )
            for k, v in self._mem_storage.items()
        ]
