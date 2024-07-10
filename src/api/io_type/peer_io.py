from pydantic.dataclasses import dataclass

from src.type.internal import PeerIdentifier, PublicKey


@dataclass(kw_only=True)
class PeerCreationRequest:
    identifier: PeerIdentifier
    public_key: PublicKey
