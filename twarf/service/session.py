
import string
import random


class SessionService():

    _LEN = 64
    _BASE = string.digits + string.ascii_letters

    def __init__(self):
        self._sessions = {}

    async def get(self, key):
        return self._sessions.get(key)

    async def put(self, key, value):
        self._sessions[key] = value

    async def new(self, value=0):
        key = ''.join(
            random.choice(self._BASE) for x in range(self._LEN)
        ).encode('ascii')
        await self.put(key, value)
        return key
