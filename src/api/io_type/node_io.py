from pydantic.dataclasses import dataclass

from src.type.internal import EndPoint, NodeIdentifier


@dataclass(kw_only=True)
class NodeCreationRequest:
    identifier: NodeIdentifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class NodeModel:
    identifier: NodeIdentifier
    endpoint: str
