from base64 import b64decode

from nacl.encoding import Base64Encoder
from nacl.signing import VerifyKey as NACLVerifyKey, SigningKey as NACLSigningKey


class EncryptionUtils:
    @staticmethod
    def verify_signature(encrypted_message: str, signing_key: str) -> str:
        return NACLVerifyKey(signing_key.encode(), Base64Encoder).verify(bytes.fromhex(encrypted_message)).decode()

    @staticmethod
    def sign(message: str, signing_key: str) -> str:
        return NACLSigningKey(signing_key.encode(), Base64Encoder).sign(bytes(message.encode())).hex()

    @staticmethod
    def decrypt_base64(encrypted_message: str) -> str: return b64decode(encrypted_message).decode()
