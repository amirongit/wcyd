from abc import ABC, abstractmethod

from src.type.entity import Node
from src.type.internal import NodeIdentifier


class FindNodeUseCase(ABC):
    @abstractmethod
    async def execute(self, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node: ...
