from typing import TypeAlias, Self

from nacl.public import PublicKey as NACLPublicKey
from nacl.encoding import Base64Encoder
from pydantic import AnyUrl, model_validator
from pydantic.dataclasses import dataclass

from src.type.enum import AsymmetricCryptographyProvider


# TODO: use the new syntax when mypy releases THE FUCKING SUPPORT
NodeIdentifier: TypeAlias = str
PeerIdentifier: TypeAlias = str
EndPoint: TypeAlias = AnyUrl


@dataclass(kw_only=True)
class UniversalPeerIdentifier:
    node: NodeIdentifier
    peer: PeerIdentifier


@dataclass(kw_only=True)
class PublicKey:
    provider: AsymmetricCryptographyProvider
    value: str

    @model_validator(mode='after')
    def _v(self: Self) -> Self:
        match self.provider:
            case AsymmetricCryptographyProvider.NACL:
                self._validate_nacl(self.value)
            case _:
                raise ValueError

        return self

    @staticmethod
    def _validate_nacl(key: str) -> None:
        try:
            NACLPublicKey(key, Base64Encoder) # type: ignore
        except Exception as e:
            raise ValueError from e
