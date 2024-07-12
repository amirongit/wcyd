from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.enum import AsymmetricCryptographyProvider
from src.type.internal import PublicKey, UniversalPeerIdentifier
from src.use_case.find_node import FindNode
from src.use_case.find_peer import FindPeer
from test.mock.infra.mock_node_client import MockNodeClient
from test.mock.infra.mock_node_repo import MockNodeRepo
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import add_external_peer, add_internal_peer, add_internal_neighbor


class TestFindPeerUseCase(IsolatedAsyncioTestCase):

    SAMPLE_PUBLIC_KEY_VALUE = (
        '-----BEGIN PGP PUBLIC KEY BLOCK-----\n'
        'mI0EZpD0xgEEANXBiz5JPurxRsPccjwcugkre3cMkA0y6lL/lTl9E9mknZTU3/ga'
        'd6SJAdmeQzwCIVa7VJSZ5C4VJde3k9vnWg0XYyxJ/IICvbuBTvHyey+8XaAx3sPK'
        '597yYUej8NXgR1M0QSI3Fz/GKHZImHd5M+2WKbEu2wGMkpnq6UnoA6NhABEBAAG0'
        'MndjeWQgKG5vc2lyd2hhdGFyZXlvdWxvb2tpbmdmb3IpIDx3Y3lkQGdpdGh1Yi5j'
        'b20+iNcEEwEKAEEWIQQ8mcCpXnnuiwPOK5p0WIgt7QTkYwUCZpD0xgIbAwUJBaOa'
        'gAULCQgHAgIiAgYVCgkICwIEFgIDAQIeBwIXgAAKCRB0WIgt7QTkY4zVBAC60cuE'
        'uEzuoXjkOqgRpFtCK8Yof5dpEH09hACQSQcdv0CLqmF1jVrM63Cjoy8l509blwzg'
        'F5WLT8HnLw6m831CTOK/iWuQEieTJ/qpdkWAp/vV/5bCQ2dCPHzrAgjISvpDuItz'
        'mkNte5idzcoV7k+4NwgceSWzQOdtgeqJkVDtPLiNBGaQ9MYBBADkrXgW/KKrvYJO'
        'ruVMVTyCcB+k+CkXjyhJpndyxOcP/kKCyu7N5uwKOtytHMfCXbSJCF0kNO1SLi7p'
        'TvxJO6U2hqTzu8hUp45qqsJhCuexN1uf4ByJo7iEXU6nzu+7i4g/Tu0jV+8dMa1H'
        'acK/gCOYA25Zmr3QdkLeQMfdv7zyIwARAQABiLwEGAEKACYWIQQ8mcCpXnnuiwPO'
        'K5p0WIgt7QTkYwUCZpD0xgIbDAUJBaOagAAKCRB0WIgt7QTkY0cgA/9yyKfltTu5'
        'KE5om1U4yRxja8r0QieVWLmIbAA/RGoKkcY25slhaWg62bzU1j5KKK6HgQP8ZReK'
        '0wMjq87F3bGI064zxngQlbDGAztKqEeuGH+2fxKwvKgtlq2LrH5Z3FHoU0xMPc/U'
        'MkAO5YIjnp/HolAZmX5d8XElQZqa8SYYfA=='
        '=7lG1\n'
        '-----END PGP PUBLIC KEY BLOCK-----'
    )

    def setUp(self) -> None:
        self._settings = NodeSettings(
            IDENTIFIER='test-node',
            ENDPOINT=AnyUrl('http://localhost:44777')
        )
        self._mock_node_client = MockNodeClient()
        self._mock_peer_repo = MockPeerRepo(self._settings)
        self._mock_node_repo = MockNodeRepo()
        self._find_node_use_case = FindNode(
            self._settings,
            self._mock_node_repo,
            self._mock_node_client
        )
        self._use_case = FindPeer(
            self._settings,
            self._mock_node_client,
            self._mock_peer_repo,
            self._find_node_use_case
        )

    async def test_normal(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'
        add_internal_peer(
            self._mock_peer_repo,
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.GPG, value=TestFindPeerUseCase.SAMPLE_PUBLIC_KEY_VALUE)
        )

        peer = await self._use_case.execute(UniversalPeerIdentifier(node=self._settings.IDENTIFIER, peer=existing_peer_identifier))

        self.assertEqual(peer.identifier.peer, existing_peer_identifier)
        self.assertEqual(peer.identifier.node, self._settings.IDENTIFIER)

    async def test_external(self) -> None:
        neighbor_identifier = 'neighbor-identifier'
        add_internal_neighbor(self._mock_node_repo, neighbor_identifier, AnyUrl('http://not-being-tested:80'))

        external_peer_identifier = 'external-peer-identifier'
        add_external_peer(
            self._mock_node_client,
            neighbor_identifier,
            external_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.GPG, value=TestFindPeerUseCase.SAMPLE_PUBLIC_KEY_VALUE)
        )

        peer = await self._use_case.execute(UniversalPeerIdentifier(node=neighbor_identifier, peer=external_peer_identifier))

        self.assertEqual(peer.identifier.node, neighbor_identifier)
        self.assertEqual(peer.identifier.peer, external_peer_identifier)
