from pydantic.dataclasses import dataclass

from src.type.internal import PeerIdentifier, PublicKey, UniversalPeerIdentifier


@dataclass(kw_only=True)
class PeerCreationRequest:
    identifier: PeerIdentifier
    public_key: PublicKey


@dataclass(kw_only=True)
class PeerModel:
    identifier: UniversalPeerIdentifier
    public_key: PublicKey
