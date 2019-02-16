
import os

import twisted.web.proxy
import twisted.internet.endpoints


class AForward():

    def __init__(self, reactor,
            host=os.environ['TWARF_FORWARD_HOST'],
            port=int(os.environ['TWARF_FORWARD_PORT'])):
        self.host = host
        self.endpoint = twisted.internet.endpoints.TCP4ClientEndpoint(
            reactor,
            host,
            port,
        )

    async def __call__(self, request):
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


def twarf_rules(reactor):
    return AForward(reactor)
