from pydantic.dataclasses import dataclass

from src.type.alias import EndPoint, Identifier, PublicKey


@dataclass(kw_only=True)
class NodeConnectionRequest:
    identifier: Identifier
    endpoint: EndPoint
    public_key: PublicKey


@dataclass(kw_only=True)
class NodeModel:
    identifier: str
    endpoint: str
    public_key: str
