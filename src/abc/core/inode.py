from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Coroutine, Self, NoReturn

from src.type.dto import ChannelDTO
from src.type.alias import Identifier, PublicKey
from src.type.exception import AlreadyAnswered, AlreadyConnected, NotFound


class INode(ABC):

    @property
    @abstractmethod
    def channel(self) -> ChannelDTO: ...

    @property
    @abstractmethod
    def identifier(self) -> Identifier: ...

    @property
    @abstractmethod
    def neighbors(self) -> Coroutine[Self, NoReturn, set[Identifier]]: ...

    @abstractmethod
    async def connect(self, node: INode) -> None: ...

    @abstractmethod
    async def find(self, questioners: set[Identifier], identifier: Identifier) -> INode: ...
