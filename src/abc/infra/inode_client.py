from __future__ import annotations

from abc import ABC, abstractmethod

from src.type.dto import ChannelDTO
from src.type.alias import Identifier
from src.abc.core.inode import INode


class INodeClient(ABC):

    @abstractmethod
    async def get_neighbors(self, channel: ChannelDTO) -> set[Identifier]: ...

    @abstractmethod
    async def connect_node(self, channel: ChannelDTO) -> None: ...

    @abstractmethod
    async def find_node(self, questioners: set[Identifier], identifier: Identifier) -> INode: ...
