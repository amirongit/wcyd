from abc import ABC, abstractmethod

from src.type.entity import Node
from src.type.internal import NodeIdentifier


class FindNodeUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: NodeIdentifier, questioners: set[NodeIdentifier] | None = None) -> Node: ...
