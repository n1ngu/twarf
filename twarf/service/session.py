
import string
import random

import twisted.internet.defer

import twarf


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

    SERVER = b'Twarf/%s' % twarf.__version__.encode()
    COOKIE = b'TWARFSESSIONID'

    def __init__(self, service, next_):
        self.service = service
        self.next = next_

    async def process(self, request):
        session_id = request.received_cookies.get(self.COOKIE)
        if not session_id:
            cookie = await self.service.new()
            request.addCookie(self.COOKIE, cookie)
            request.temporary_redirect(request.uri)
            request.setHeader(b'server', self.SERVER)
            request.setHeader(b'date', twisted.web.http.datetimeToString())
            request.finish()
        else:
            await self.next.process(request)
