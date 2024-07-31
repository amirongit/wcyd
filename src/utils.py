from base64 import b64decode

from nacl.encoding import Base64Encoder
from nacl.signing import VerifyKey as NACLVerifyKey


class EncryptionUtils:
    @staticmethod
    def verify_signature(encrypted_message: str, signing_key: str) -> str:
        return NACLVerifyKey(
            signing_key.encode(),
            Base64Encoder
        ).verify(
            Base64Encoder.decode(encrypted_message.encode())
        ).decode()

    @staticmethod
    def decrypt_base64(encrypted_message: str) -> str: return b64decode(encrypted_message).decode()
