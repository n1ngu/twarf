
import string
import random

import twisted.internet.defer


def deferred(coroutine):
    def deferrer(*args, **kwargs):
        return twisted.internet.defer.ensureDeferred(
            coroutine(*args, **kwargs)
        )
    return deferrer


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


class SetCookie():

    def __init__(self, service, next_):
        self.service = service
        self.next = next_

    async def process(self, request):
        session_id = self.received_cookies.get(b'TWARFSESSIONID')
        if not session_id:
            cookie = await self.service.new()
        else:
            await self.next(request)
