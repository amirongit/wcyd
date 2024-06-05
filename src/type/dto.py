from pydantic.dataclasses import dataclass
from pydantic.networks import AnyUrl

from src.type.alias import PublicKey


@dataclass(kw_only=True)
class ChannelDTO:
    endpoint: AnyUrl
    public_key: PublicKey
