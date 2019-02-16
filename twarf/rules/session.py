
import os

import twisted.web.http

import twarf
import twarf.service.session

from . import TwarfRule
from .flow import If
from .forward import AForward


SERVER = b'Twarf/%s' % twarf.__version__.encode()
COOKIE = b'TWARFSESSIONID'


class GetCookie(TwarfRule):

    async def __call__(self, request):
        return request.received_cookies.get(COOKIE)


class SetCookie(TwarfRule):

    def __init__(self, service):
        self.service = service

    async def __call__(self, request):
        cookie = await self.service.new()
        request.addCookie(COOKIE, cookie)
        request.temporary_redirect(request.uri)
        request.setHeader(b'server', SERVER)
        request.setHeader(b'date', twisted.web.http.datetimeToString())
        request.finish()


def twarf_rules(reactor) -> TwarfRule:

    session_service = twarf.service.session.SessionService()

    return If(
        test=GetCookie(),
        then=AForward(reactor),
        orelse=SetCookie(session_service)
    )
