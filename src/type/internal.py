import re
from typing import TypeAlias, Self

from pydantic import AnyUrl, ValidationError, model_validator
from pydantic.dataclasses import dataclass

from src.type.enum import AsymmetricCryptographyProvider


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
            case AsymmetricCryptographyProvider.SSH:
                self._validate_ssh_pub_key(self.value)
            case AsymmetricCryptographyProvider.GPG:
                self._validate_gpg_pub_key(self.value)
            case _:
                raise ValueError

        return self

    @staticmethod
    def _validate_ssh_pub_key(key: str) -> None:
        if not re.match(
            r'^(ssh-rsa|ssh-dss|ecdsa-sha2-nistp256|ecdsa-sha2-nistp384|ecdsa-sha2-nistp521|ssh-ed25519)\s+([A-Za'
            r'-z0-9+/]+[=]{0,3})\s+(.+)$',
            key
        ):
            raise ValueError

    @staticmethod
    def _validate_gpg_pub_key(key: str) -> None:
        if not re.match(
            r'^-----BEGIN PGP PUBLIC KEY BLOCK-----\s+(Version: .+\s+)?(.+\s+)+-----END PGP PUBLIC KEY BLOCK-----$',
            key
        ):
            raise ValueError
