from pydantic.dataclasses import dataclass

from src.type.internal import EndPoint, NodeIdentifier


@dataclass(kw_only=True)
class NodeConnectionRequest:
    identifier: NodeIdentifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class NodeModel:
    identifier: str
    endpoint: str
