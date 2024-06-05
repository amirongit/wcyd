from __future__ import annotations

from abc import ABC, abstractmethod

from src.type import ChannelDTO, Identifier, PublicKey


class INode(ABC):

    @property
    @abstractmethod
    def channel(self) -> ChannelDTO: ...

    @property
    @abstractmethod
    def identifier(self) -> Identifier: ...

    @property
    @abstractmethod
    def neighbors(self) -> set[Identifier]: ...

    @abstractmethod
    def connect(self, node: INode) -> None: ...

    @abstractmethod
    def find(self, questioners: set[Identifier], identifier: Identifier) -> INode: ...
