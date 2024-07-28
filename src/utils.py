from nacl.encoding import Base64Encoder
from nacl.signing import VerifyKey as NACLVerifyKey


class EncryptionUtils:
    @staticmethod
    def verify_signature(encrypted_message: str, signing_key: str) -> tuple[bool, str | None]:
        try:
            return True, NACLVerifyKey(
                signing_key.encode(),
                Base64Encoder
            ).verify(
                Base64Encoder.decode(encrypted_message.encode())
            ).decode()
        except Exception:
            return False, None


if __name__ == '__main__':
    message = 'gC1BL/imXmaruCWDj4QINtYG85O8HWDnGubiIf/0kwvOKP96TH9/m1LQsgspQKg17Ak981u+FDoo5/ZvsjlqC2xvY2FsQGFtaXJ0aGVob3NzZWluOjE3MjIxOTA2NzMuNTgxMDA1'
    sgk = 'QW1j319IkhjIGVmOBZAJt0Tsqs6d4nWbA5n6l1iupj8='
    print(EncryptionUtils.verify_signature(message, sgk))
