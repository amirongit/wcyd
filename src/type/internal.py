from typing import Self, TypeAlias

from nacl.encoding import Base64Encoder
from nacl.public import PublicKey as NACLPublicKey
from nacl.signing import SigningKey as NACLSigningKey
from pydantic import AnyUrl, model_validator
from pydantic.dataclasses import dataclass

NodeIdentifier: TypeAlias = str
PeerIdentifier: TypeAlias = str
PeerCredentials: TypeAlias = str
EndPoint: TypeAlias = AnyUrl


@dataclass(kw_only=True)
class UniversalPeerIdentifier:
    node: NodeIdentifier
    peer: PeerIdentifier


@dataclass(kw_only=True)
class Keyring:
    signing: str
    encryption: str

    @model_validator(mode="after")
    def _v(self: Self) -> Self:
        try:
            NACLPublicKey(self.encryption.encode(), Base64Encoder)
            NACLSigningKey(self.signing.encode(), Base64Encoder)
        except Exception as e:
            raise ValueError from e

        return self
