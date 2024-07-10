from typing import TypedDict
from src.abc.infra.ipeer_repo import IPeerRepo
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import PeerIdentifier, PublicKey


class MockRepoPeerObjectModel(TypedDict):
    key_provider: str
    key_value: str


class MockPeerRepo(IPeerRepo):
    def __init__(self) -> None:
        self._mem_storage: dict[PeerIdentifier, MockRepoPeerObjectModel] = dict()

    async def exists(self, identifier: PeerIdentifier) -> bool:
        return identifier in self._mem_storage

    async def create(self, identifier: PeerIdentifier, public_key: PublicKey) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        self._mem_storage[identifier] = {'key_provider': public_key.provider.name, 'key_value': public_key.value}

    async def delete(self, identifier: PeerIdentifier) -> None:
        try:
            self._mem_storage.pop(identifier)
        except KeyError:
            raise DoesNotExist
