from typing import TypedDict
from aiohttp import ClientSession
from pydantic.networks import AnyUrl

from src.abc.infra.inode_client import INodeClient
from src.type.internal import EndPoint, Identifier
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound


class APIClientNodeObjectModel(TypedDict):
    identifier: str
    endpoint: str


class NodeClient(INodeClient):

    def __init__(self) -> None:
        self._session = ClientSession()

    async def get_neighbors(self, host: Node) -> list[Node]:
        async with self._session as sess:
            async with sess.get(f'{host.endpoint}/nodes') as resp:
                if resp.status == 200:

                    result: list[Node] = list()

                    obj: APIClientNodeObjectModel
                    for obj in await resp.json():
                        result.append(Node(identifier=obj['identifier'], endpoint=AnyUrl(obj['endpoint'])))

                    return result

        raise Exception

    async def connect(self, host: Node, identifier: Identifier, endpoint: EndPoint) -> None:

        body: APIClientNodeObjectModel = {'identifier': identifier, 'endpoint': str(endpoint)}

        async with self._session as sess:
            async with sess.post(f'{host.endpoint}/nodes', json=body) as resp:
                match resp.status:
                    case 201:
                        return None
                    case 409:
                        raise AlreadyExists
                    case _:
                        raise Exception

    async def find(self, host: Node, questioners: set[Identifier], identifier: Identifier) -> Node:
        async with self._session as sess:
            async with sess.get(f'{host.endpoint}/nodes/{identifier}', params={'questioners': questioners}
            ) as resp:
                match resp.status:
                    case 200:
                        return Node(**await resp.json())
                    case 404:
                        raise NotFound
                    case 409:
                        raise AlreadyAnswered
                    case _:
                        raise Exception
