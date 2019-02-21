
import os
import asyncio

import twisted.web.proxy
import twisted.internet.endpoints

from . import TwarfRule


class Forward(TwarfRule):

    def __init__(self, reactor,
                 host=os.environ.get('TWARF_FORWARD_HOST'),
                 port=int(os.environ.get('TWARF_FORWARD_PORT', 0))):
        self.host = host
        self.endpoint = twisted.internet.endpoints.TCP4ClientEndpoint(
            reactor,
            host,
            port,
        )

    async def process(self, request):
        request.requestHeaders.setRawHeaders(
            b"host",
            [self.host.encode('ascii')]
        )
        clientFactory = twisted.web.proxy.ProxyClientFactory(
            request.method, request.uri, request.clientproto,
            request.getAllHeaders(),
            request.content.read(),
            request
        )
        await self.endpoint.connect(clientFactory)


class Throttle(TwarfRule):

    def __init__(self, fwd, delay=0):
        self.fwd = fwd
        self.delay = delay

    async def process(self, request):
        await asyncio.sleep(self.delay)
        await self.fwd(request)


def twarf_rules(reactor):
    return Forward(reactor)
