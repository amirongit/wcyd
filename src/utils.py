from base64 import b64decode

from nacl.encoding import Base64Encoder
from nacl.signing import SigningKey as NACLSigningKey
from nacl.signing import VerifyKey as NACLVerifyKey

from src.type.internal import PeerCredentials, UniversalPeerIdentifier


class EncryptionUtils:
    @staticmethod
    def verify_signature(encrypted_message: str, signing_key: str) -> str:
        return NACLVerifyKey(signing_key.encode(), Base64Encoder).verify(bytes.fromhex(encrypted_message)).decode()

    @staticmethod
    def sign(message: str, signing_key: str) -> str:
        return NACLSigningKey(signing_key.encode(), Base64Encoder).sign(bytes(message.encode())).hex()

    @staticmethod
    def decrypt_base64(encrypted_message: str) -> str:
        return b64decode(encrypted_message).decode()


class AuthUtils:
    @staticmethod
    def extract_identifier(credentials: PeerCredentials) -> UniversalPeerIdentifier:
        peer_identifier, node_identifier = (
            EncryptionUtils.decrypt_base64(credentials).removeprefix("Basic ").split(":")[0].split("@")
        )
        return UniversalPeerIdentifier(peer=peer_identifier, node=node_identifier)
