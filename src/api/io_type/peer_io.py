from pydantic.dataclasses import dataclass

from src.type.internal import Keyring, PeerIdentifier, UniversalPeerIdentifier


@dataclass(kw_only=True)
class PeerCreationRequest:
    identifier: PeerIdentifier
    keyring: Keyring


@dataclass(kw_only=True)
class PeerModel:
    identifier: UniversalPeerIdentifier
    keyring: Keyring
