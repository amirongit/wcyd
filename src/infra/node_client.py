from typing import TypedDict
from aiohttp import ClientSession

from src.abc.infra.inode_client import INodeClient
from src.type.alias import EndPoint, Identifier, PublicKey
from src.type.entity import Node
from src.type.exception import AlreadyAnswered, AlreadyExists, NotFound


PATHS = {
    'GET_NEIGHBORS': '/nodes',
    'GET_NODE': '/nodes/{identifier}',
    'REGISTER': '/nodes',
}


class APINodeObjectModel(TypedDict):
    identifier: str
    endpoint: str
    public_key: str


class NodeClient(INodeClient):

    def __init__(self) -> None:
        self._session = ClientSession()

    async def get_neighbors(self, host: Node) -> list[Node]:
        async with self._session as sess:
            async with sess.get(f'{host.endpoint}/{PATHS['GET_NEIGHBORS']}') as resp:
                if resp.status == 200:

                    result: list[Node] = list()

                    obj: APINodeObjectModel
                    for obj in await resp.json():
                        result.append(
                            Node(
                                identifier=obj['identifier'],
                                endpoint=obj['endpoint'], # type: ignore
                                public_key=obj['public_key']
                            )
                        )

                    return result

        raise Exception

    async def connect(self, host: Node, identifier: Identifier, endpoint: EndPoint, public_key: PublicKey) -> None:

        body: APINodeObjectModel = {'identifier': identifier, 'endpoint': str(endpoint), 'public_key': public_key}

        async with self._session as sess:
            async with sess.post(f'{host.endpoint}/{PATHS['REGISTER']}', json=body) as resp:
                match resp.status:
                    case 201:
                        return None
                    case 409:
                        raise AlreadyExists
                    case _:
                        raise Exception

    async def find(self, host: Node, questioners: set[Identifier], identifier: Identifier) -> Node:
        async with self._session as sess:
            async with sess.get(
                f'{host.endpoint}/{PATHS['GET_NODE']}'.format(identifier=identifier),
                params={'questioners': questioners}
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
