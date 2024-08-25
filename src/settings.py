from json import loads

from pydantic import AnyUrl, Field, RedisDsn
from pydantic.dataclasses import dataclass


@dataclass(kw_only=True)
class NodeSettings:
    IDENTIFIER: str
    ENDPOINT: AnyUrl


@dataclass(kw_only=True)
class RedisSettings:
    DSN: RedisDsn


@dataclass(kw_only=True)
class AuthenticationSettings:
    TIME_WINDOW: int = Field(gt=0)


@dataclass(kw_only=True)
class Settings:
    LOCAL_NODE: NodeSettings
    REDIS: RedisSettings
    AUTHENTICATION: AuthenticationSettings


def read_settings() -> Settings:
    with open('./settings.json', 'r') as f:
        return Settings(**loads(f.read()))
