from typing import TypedDict

from src.abc.infra.inode_repo import INodeRepo
from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node
from src.type.exception import AlreadyExists, NotFound


class MockRepoNodeObjectModel(TypedDict):
    endpoint: str
    public_key: str


class MockNodeRepo(INodeRepo):

    def __init__(self) -> None:
        self._mem_storage: dict[Identifier, MockRepoNodeObjectModel] = dict()

    async def get(self, identifier: Identifier) -> Node:
        if (obj := self._mem_storage.get(identifier)) is not None:
            return Node(identifier=identifier, **obj) # type: ignore

        raise NotFound

    async def exists(self, identifier: Identifier) -> bool:
        return identifier in self._mem_storage

    async def create(self, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        self._mem_storage[identifier] = {'endpoint': str(endpoint), 'public_key': public_key}

    async def all(self) -> list[Node]:
        return [
            Node(
                identifier=k,
                endpoint=v['endpoint'], # type: ignore
                public_key=v['public_key']
            ) for k, v in self._mem_storage.items()
        ]
