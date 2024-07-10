from pydantic.dataclasses import dataclass

from src.type.internal import NodeIdentifier, EndPoint, PublicKey, UniversalPeerIdentifier


@dataclass(kw_only=True)
class Node:
    identifier: NodeIdentifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class Peer:
    identifier: UniversalPeerIdentifier
    public_key: PublicKey
