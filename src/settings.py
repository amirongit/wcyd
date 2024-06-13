from json import loads

from pydantic.dataclasses import dataclass
from pydantic.networks import AnyUrl
from pydantic import RedisDsn


@dataclass(kw_only=True)
class NodeSettings:
    IDENTIFIER: str
    PUBLIC_KEY: str
    ENDPOINT: AnyUrl


@dataclass(kw_only=True)
class RedisSettings:
    DSN: RedisDsn


@dataclass(kw_only=True)
class Settings:
    LOCAL_NODE: NodeSettings
    REDIS: RedisSettings


SETTINGS: Settings
with open('./settings.json', 'r') as f:
    SETTINGS = Settings(**loads(f.read()))
