
import http

import twisted.web.http

import twarf

from . import TwarfRule


SERVER = b'Twarf/%s' % twarf.__version__.encode()


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
