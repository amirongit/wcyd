from typing import TypeAlias, Self

from nacl.public import PublicKey as NACLPublicKey
from nacl.signing import SigningKey as NACLSigningKey
from nacl.encoding import Base64Encoder
from pydantic import AnyUrl, model_validator
from pydantic.dataclasses import dataclass


# TODO: use the new syntax when mypy releases THE FUCKING SUPPORT
NodeIdentifier: TypeAlias = str
PeerIdentifier: TypeAlias = str
EndPoint: TypeAlias = AnyUrl


@dataclass(kw_only=True)
class UniversalPeerIdentifier:
    node: NodeIdentifier
    peer: PeerIdentifier


@dataclass(kw_only=True)
class Keyring:
    signing: str
    encryption: str

    @model_validator(mode='after')
    def _v(self: Self) -> Self:
        try:
            NACLPublicKey(self.encryption, Base64Encoder) # type: ignore
            NACLSigningKey(self.signing, Base64Encoder) # type: ignore
        except Exception as e:
            raise ValueError from e

        return self
