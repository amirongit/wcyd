from pydantic.dataclasses import dataclass

from src.type.internal import UniversalPeerIdentifier


@dataclass(kw_only=True)
class MessageTransferRequest:
    source: UniversalPeerIdentifier
    content: str
