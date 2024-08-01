from pydantic.dataclasses import dataclass


@dataclass(kw_only=True)
class MessageTransferRequest:
    content: str
