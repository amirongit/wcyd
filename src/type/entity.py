from pydantic.dataclasses import dataclass

from src.type.alias import Identifier, PublicKey, EndPoint


@dataclass(kw_only=True)
class Node:
    identifier: Identifier
    endpoint: EndPoint
    public_key: PublicKey
