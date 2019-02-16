
import cryptography.fernet


class CryptoService():

    # FIXME: I am synchronous!

    def __init__(self, keys: list):
        self.key = cryptography.fernet.MultiFernet([
            cryptography.fernet.Fernet(key)
            for key in keys
        ])
        assert b'assert' == self.key.decrypt(self.key.decrypt(b'assert'))

    async def encrypt(self, message: bytes) -> bytes:
        return self.key.encrypt(message)

    async def decrypt(self, message: bytes) -> bytes:
        return self.key.decrypt(message)
