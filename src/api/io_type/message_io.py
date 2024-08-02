from uuid import UUID
from pydantic.dataclasses import dataclass

from src.type.internal import UniversalPeerIdentifier


@dataclass(kw_only=True)
class MessageTransferRequest:
    content: str


@dataclass(kw_only=True)
class MessageModel:
    identifier: UUID
    source: UniversalPeerIdentifier
    content: str
