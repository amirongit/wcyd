from typing import TypeAlias

from pydantic.networks import HttpUrl


# TODO
# use the new syntax when mypy starts supporting it
Identifier: TypeAlias = str
PublicKey: TypeAlias = str
EndPoint: TypeAlias = HttpUrl
