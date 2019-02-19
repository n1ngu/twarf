
import twarf._utils


class SessionService():

    # FIXME: I am synchronous!

    _LEN = 64

    def __init__(self):
        self._sessions = {}

    async def get(self, key):
        return self._sessions.get(key)

    async def put(self, key, value):
        self._sessions[key] = value

    async def new(self, value=0):
        key = twarf._utils.build_random_string(self._LEN)
        await self.put(key, value)
        return key
