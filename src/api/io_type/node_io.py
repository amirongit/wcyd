from pydantic.dataclasses import dataclass

from src.type.internal import EndPoint, NodeIdentifier


@dataclass(kw_only=True)
class NodeModel:
    identifier: NodeIdentifier
    endpoint: EndPoint
