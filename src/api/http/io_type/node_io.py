from pydantic.dataclasses import dataclass


@dataclass(kw_only=True)
class NodeConnectionRequest:
    identifier: str
    endpoint: str
    public_key: str
