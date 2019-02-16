
import http

import twisted.web.http

import twarf

from . import TwarfRule


SERVER = b'Twarf/%s' % twarf.__version__.encode()


class If(TwarfRule):

    def __init__(self, test, then, orelse):
        self.test = test
        self.then = then
        self.orelse = orelse

    async def __call__(self, request):
        if await self.test(request):
            await self.then(request)
        else:
            await self.orelse(request)


class Finish(TwarfRule):

    async def __call__(self, request):
        request.setHeader(b'server', SERVER)
        request.setHeader(b'date', twisted.web.http.datetimeToString())
        request.finish()


class HttpStatus(Finish):

    http_status = None

    async def __call__(self, request):
        request.setResponseCode(self.http_status)
        await super().__call__(request)


class TempRedirect(Finish):

    async def __call__(self, request):
        request.temporary_redirect(request.uri)
        await super().__call__(request)


class Unauthorized(HttpStatus):
    http_status = http.HTTPStatus.UNAUTHORIZED


class BadRequest(HttpStatus):
    http_status = http.HTTPStatus.BAD_REQUEST


class InternalServerError(HttpStatus):
    http_status = http.HTTPStatus.INTERNAL_SERVER_ERROR


class Unreachable(InternalServerError):

    async def __call__(self, request):
        # FIXME: issue warning through logging service
        print("FATAL: request reached unreachable rule")
        await super().__call__(request)
