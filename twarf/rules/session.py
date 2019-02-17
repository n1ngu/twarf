
import twarf.service.session

from . import TwarfRule
from . import TwarfTest
from .flow import If
from .http import TempRedirect
from .forward import Forward


COOKIE = b'TWARFSESSIONID'


class SetCookie(TempRedirect):

    def __init__(self, service):
        self.service = service

    async def process(self, request):
        cookie = await self.service.new()
        request.addCookie(COOKIE, cookie)
        await super().process(request)


class MatchCookie(TwarfTest):

    def __init__(self, service, value):
        self.service = service
        self.value = value

    async def test(self, request):
        cookie = request.received_cookies.get(COOKIE)
        session = await self.service.get(cookie)
        return session == self.value


def twarf_rules(reactor) -> TwarfRule:

    session_service = twarf.service.session.SessionService()

    return If(
        test=MatchCookie(session_service, 0),
        then=Forward(reactor),
        orelse=SetCookie(session_service),
    )
