from pydantic.dataclasses import dataclass

from src.type.alias import EndPoint, Identifier


@dataclass(kw_only=True)
class NodeConnectionRequest:
    identifier: Identifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class NodeModel:
    identifier: str
    endpoint: str
