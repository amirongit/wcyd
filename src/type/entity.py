from pydantic.dataclasses import dataclass

from src.type.alias import Identifier, EndPoint


@dataclass(kw_only=True)
class Node:
    identifier: Identifier
    endpoint: EndPoint
