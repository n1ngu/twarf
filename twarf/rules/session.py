
import twarf.service.session

from . import TwarfRule
from .flow import If
from .http import TempRedirect
from .http import BadRequest
from .forward import Forward


COOKIE = b'TWARFSESSIONID'


class GetCookie(TwarfRule):

    async def __call__(self, request):
        return request.received_cookies.get(COOKIE)


class SetCookie(TempRedirect):

    def __init__(self, service):
        self.service = service

    async def __call__(self, request):
        cookie = await self.service.new()
        request.addCookie(COOKIE, cookie)
        await super().__call__(request)


class MatchCookie(TwarfRule):

    def __init__(self, service, value):
        self.service = service
        self.value = value

    async def __call__(self, request):
        cookie = request.received_cookies.get(COOKIE)
        session = await self.service.get(cookie)
        return session == self.value


def twarf_rules(reactor) -> TwarfRule:

    session_service = twarf.service.session.SessionService()

    return If(
        test=MatchCookie(session_service, 0),
        then=Forward(reactor),
        orelse=If(
            test=GetCookie(),
            # Too agressive? Cookies may get naturally old, or a simple
            # restart of a naive memory session service may forgot them
            then=BadRequest(),
            orelse=SetCookie(session_service),
        ),
    )
