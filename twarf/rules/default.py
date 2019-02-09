
import twisted.web.proxy
import twisted.web.http

import twarf

SERVER = b'Twarf/%s' % twarf.__version__
COOKIE = b'TWARFSESSIONID'


def has_cookie(request):
    return bool(request.received_cookies.get(COOKIE))


def true(request):
    return True


def forward(request):
    request.requestHeaders.setRawHeaders(
        b"host",
        [request.channel.factory.host.encode('ascii')]
    )
    clientFactory = twisted.web.proxy.ProxyClientFactory(
        request.method, request.uri, request.clientproto,
        request.getAllHeaders(),
        request.content.read(),
        request
    )
    request.channel.factory.endpoint.connect(clientFactory)


def set_cookie(request):
    cookie = b'0000000000000'
    request.addCookie(COOKIE, cookie)
    request.temporary_redirect(request.uri)
    request.setHeader(b'server', SERVER)
    request.setHeader(b'date', twisted.web.http.datetimeToString())
    request.finish()


TWARF_RULES = [
    (has_cookie, forward),
    (true, set_cookie),
]
