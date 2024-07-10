from abc import ABC, abstractmethod

from src.type.internal import EndPoint, NodeIdentifier


class ConnectNodeUseCase(ABC):
    @abstractmethod
    async def execute(self, identifier: NodeIdentifier, endpoint: EndPoint) -> None: ...
