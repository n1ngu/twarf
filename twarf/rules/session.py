
import os

import twisted.web.http

import twarf
import twarf.service.session

from .flow import If
from .forward import AForward


SERVER = b'Twarf/%s' % twarf.__version__.encode()
COOKIE = b'TWARFSESSIONID'


class GetCookie():

    async def process(self, request):
        return request.received_cookies.get(COOKIE)


class SetCookie():

    def __init__(self, service):
        self.service = service

    async def process(self, request):
        cookie = await self.service.new()
        request.addCookie(COOKIE, cookie)
        request.temporary_redirect(request.uri)
        request.setHeader(b'server', SERVER)
        request.setHeader(b'date', twisted.web.http.datetimeToString())
        request.finish()


def twarf_rules(reactor):
    session_service = twarf.service.session.SessionService()
    rules = If(
        test=GetCookie(),
        then=AForward(reactor),
        orelse=SetCookie(session_service)
    )
    return rules.process
