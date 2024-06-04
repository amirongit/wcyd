from typing import TypeAlias

from pydantic.dataclasses import dataclass
from pydantic.networks import AnyUrl

Identifier: TypeAlias = str
PublicKey: TypeAlias = str


@dataclass(kw_only=True)
class ChannelDTO:
    endpoint: AnyUrl
    public_key: PublicKey


class NodeAlreadyIsConnected(Exception):
    pass


class NodeAlreadyAnswered(Exception):
    pass


class NodeNotFound(Exception):
    pass
