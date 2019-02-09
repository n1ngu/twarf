
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

    async def _get(self, key):
        return self._sessions.get(key)

    def get(self, key):
        return twisted.internet.defer.ensureDeferred(
            self._get(key)
        )

    async def _put(self, key, value):
        self._sessions[key] = value

    def put(self, key, value):
        return twisted.internet.defer.ensureDeferred(
            self._put(key, value)
        )

    async def _new(self, value=0):
        key = ''.join(
            random.choice(self._BASE) for x in range(self._LEN)
        ).encode('ascii')
        await self._put(key, value)
        return key

    def new(self, value=0):
        return twisted.internet.defer.ensureDeferred(
            self._new(value)
        )
