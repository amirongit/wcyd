from typing import TypedDict
from uuid import UUID

from aiohttp import ClientSession
from pydantic import AnyUrl

from src.abc.infra.inode_client import INodeClient
from src.type.internal import EndPoint, NodeIdentifier, Keyring, PeerCredentials, UniversalPeerIdentifier
from src.type.entity import Message, Node, Peer
from src.type.exception import AlreadyAnswered, AlreadyExists, DoesNotExist, UnAuthenticated


class APIClientNodeObjectModel(TypedDict):
    identifier: str
    endpoint: str


class APIClientUniversalIdentifierObjectModel(TypedDict):
    node: str
    peer: str


class APIClientKeyringObjectModel(TypedDict):
    signing: str
    encryption: str


class APIClientPeerObjectModel(TypedDict):
    identifier: APIClientUniversalIdentifierObjectModel
    keyring: APIClientKeyringObjectModel


class APIClientShallowMessageObjectModel(TypedDict):
    content: str


class APIClientMessageObjectMode(TypedDict):
    identifier: str
    source: APIClientUniversalIdentifierObjectModel
    content: str


class NodeClient(INodeClient):

    def __init__(self) -> None:
        self._session = ClientSession()

    async def connect_node(self, host: Node, identifier: NodeIdentifier, endpoint: EndPoint) -> None:
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

    async def find_node(self, host: Node, questioners: set[NodeIdentifier], identifier: NodeIdentifier) -> Node:
        async with self._session as sess:
            async with sess.get(f'{host.endpoint}/nodes/{identifier}', params={'questioners': questioners}) as resp:
                match resp.status:
                    case 200:
                        body: APIClientNodeObjectModel = await resp.json()
                        return Node(identifier=body['identifier'], endpoint=AnyUrl(body['endpoint']))
                    case 404:
                        raise DoesNotExist
                    case 409:
                        raise AlreadyAnswered
                    case _:
                        raise Exception

    async def find_peer(self, host: Node, identifier: UniversalPeerIdentifier) -> Peer:
        async with self._session as sess:
            async with sess.get(f'{host.endpoint}/nodes/{identifier.node}/peers/{identifier.peer}') as resp:
                match resp.status:
                    case 200:
                        body: APIClientPeerObjectModel = await resp.json()
                        return Peer(
                            identifier=UniversalPeerIdentifier(
                                peer=body['identifier']['peer'],
                                node=body['identifier']['node']
                            ),
                            keyring=Keyring(
                                signing=body['keyring']['signing'],
                                encryption=body['keyring']['encryption']
                            )
                        )
                    case 404:
                        raise DoesNotExist
                    case _:
                        raise Exception

    async def send_message(
        self,
        host: Node,
        credentials: PeerCredentials,
        target: UniversalPeerIdentifier,
        content: str
    ) -> None:
        body: APIClientShallowMessageObjectModel = {'content': content}
        async with self._session as sess:
            async with sess.post(
                f'{host.endpoint}/nodes/{target.node}/peers/{target.peer}/messages',
                json=body,
                headers={'Authorization': f'Basic {credentials}'}
            ) as resp:
                match resp.status:
                    case 201:
                        pass
                    case 401:
                        raise UnAuthenticated
                    case 404:
                        raise DoesNotExist
                    case _:
                        raise Exception

    async def get_related_messages(
        self,
        host: Node,
        target: UniversalPeerIdentifier,
        credentials: PeerCredentials
    ) -> list[Message]:
        async with self._session as sess:
            async with sess.get(
                f'{host.endpoint}/messages', headers={'Authorization': f'Basic {credentials}'}
            ) as resp:
                match resp.status:
                    case 200:
                        body: list[APIClientMessageObjectMode] = await resp.json()
                        return [
                            Message(
                                identifier=UUID(obj['identifier']),
                                source=UniversalPeerIdentifier(
                                    node=obj['source']['node'],
                                    peer=obj['source']['peer']
                                ),
                                target=target,
                                content=obj['content']
                            ) for obj in body
                        ]
                    case 401:
                        raise UnAuthenticated
                    case _:
                        raise Exception
