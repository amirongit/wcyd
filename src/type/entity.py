from pydantic.dataclasses import dataclass

from src.type.internal import Identifier, EndPoint


@dataclass(kw_only=True)
class Node:
    identifier: Identifier
    endpoint: EndPoint


@dataclass(kw_only=True)
class Peer:
    pass
