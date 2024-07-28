from typing import TypedDict
from src.abc.infra.ipeer_repo import IPeerRepo
from src.settings import NodeSettings
from src.type.entity import Peer
from src.type.exception import AlreadyExists, DoesNotExist
from src.type.internal import PeerIdentifier, Keyring, UniversalPeerIdentifier


class MockRepoPeerObjectModel(TypedDict):
    signing_key: str
    encryption_key: str


class MockPeerRepo(IPeerRepo):
    def __init__(self, node_settings: NodeSettings) -> None:
        self._mem_storage: dict[PeerIdentifier, MockRepoPeerObjectModel] = dict()
        self._settings = node_settings

    async def get(self, identifier: PeerIdentifier) -> Peer:
        try:
            obj = self._mem_storage[identifier]
            return Peer(
                identifier=UniversalPeerIdentifier(peer=identifier, node=self._settings.IDENTIFIER),
                keyring=Keyring(
                    signing=obj['signing_key'],
                    encryption=obj['encryption_key']
                )
            )
        except KeyError:
            raise DoesNotExist

    async def exists(self, identifier: PeerIdentifier) -> bool:
        return identifier in self._mem_storage

    async def create(self, identifier: PeerIdentifier, keyring: Keyring) -> None:
        if await self.exists(identifier):
            raise AlreadyExists

        self._mem_storage[identifier] = {'signing_key': keyring.signing, 'encryption_key': keyring.encryption}

    async def delete(self, identifier: PeerIdentifier) -> None:
        try:
            self._mem_storage.pop(identifier)
        except KeyError:
            raise DoesNotExist
