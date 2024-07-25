from unittest import IsolatedAsyncioTestCase

from pydantic import AnyUrl

from src.settings import NodeSettings
from src.type.enum import AsymmetricCryptographyProvider
from src.type.exception import AlreadyExists
from src.type.internal import PublicKey
from src.use_case.add_peer import AddPeer
from test.mock.infra.mock_peer_repo import MockPeerRepo
from test.utils import get_internal_peer


class TestAddPeerUseCase(IsolatedAsyncioTestCase):

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
        self._peer_repo = MockPeerRepo(self._settings)
        self._use_case = AddPeer(self._peer_repo)

    async def test_normal(self) -> None:
        test_peer_identifier = 'test-peer-identifier'

        await self._use_case.execute(
            test_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.GPG, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        peer = await get_internal_peer(self._peer_repo, test_peer_identifier)

        self.assertEqual(peer.identifier.peer, test_peer_identifier)
        self.assertEqual(peer.public_key.provider, AsymmetricCryptographyProvider.GPG)
        self.assertEqual(peer.public_key.value, self.SAMPLE_PUBLIC_KEY_VALUE)

    async def test_duplicated_identifier(self) -> None:
        existing_peer_identifier = 'existing-peer-identifier'
        await self._use_case.execute(
            existing_peer_identifier,
            PublicKey(provider=AsymmetricCryptographyProvider.GPG, value=self.SAMPLE_PUBLIC_KEY_VALUE)
        )

        with self.assertRaises(AlreadyExists):
            await self._use_case.execute(
                existing_peer_identifier,
                PublicKey(provider=AsymmetricCryptographyProvider.GPG, value=self.SAMPLE_PUBLIC_KEY_VALUE)
            )
