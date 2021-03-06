
import http

import twisted.web.http
import twisted.web.proxy
import twisted.internet.defer


class TwarfRequest(twisted.web.http.Request):

    def __init__(
            self, channel,
            queued=twisted.web.http._QUEUED_SENTINEL):
        twisted.web.http.Request.__init__(self, channel, queued)

    def process(self):
        coro = self.channel.factory.rules(self)
        self.deferred = twisted.internet.defer.ensureDeferred(coro)

    def temporary_redirect(self, url):
        self.setResponseCode(http.HTTPStatus.TEMPORARY_REDIRECT)
        self.setHeader(b"location", url)

    def connectionLost(self, reason):
        super().connectionLost(reason)


class TwarfProxy(twisted.web.http.HTTPChannel):
    requestFactory = TwarfRequest


class TwarfFactory(twisted.internet.protocol.ServerFactory):

    protocol = TwarfProxy

    def __init__(self, rules):
        self.rules = rules

    def log(self, *args, **kwargs):
        pass
