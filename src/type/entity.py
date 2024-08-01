from uuid import UUID

from pydantic.dataclasses import dataclass

from src.type.internal import NodeIdentifier, EndPoint, Keyring, UniversalPeerIdentifier


@dataclass(kw_only=True)
class Node:
    identifier: NodeIdentifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class Peer:
    identifier: UniversalPeerIdentifier
    keyring: Keyring


@dataclass(kw_only=True)
class Message:
    identifier: UUID
    source: UniversalPeerIdentifier
    target: UniversalPeerIdentifier
    content: str
