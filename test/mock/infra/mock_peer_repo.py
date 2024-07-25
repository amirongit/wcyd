from typing import TypedDict
from src.abc.infra.ipeer_repo import IPeerRepo
from src.settings import NodeSettings
from src.type.entity import Peer
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import PeerIdentifier, PublicKey, UniversalPeerIdentifier


class MockRepoPeerObjectModel(TypedDict):
    key_provider: str
    key_value: str


class MockPeerRepo(IPeerRepo):
    def __init__(self, node_settings: NodeSettings) -> None:
        self._mem_storage: dict[PeerIdentifier, MockRepoPeerObjectModel] = dict()
        self._settings = node_settings

    async def get(self, identifier: PeerIdentifier) -> Peer:
        try:
            obj = self._mem_storage[identifier]
            return Peer(
                identifier=UniversalPeerIdentifier(peer=identifier, node=self._settings.IDENTIFIER),
                public_key=PublicKey(
                    provider=AsymmetricCryptographyProvider[obj['key_provider']],
                    value=obj['key_value']
                )
            )
        except KeyError:
            raise DoesNotExist

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
