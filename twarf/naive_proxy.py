
import importlib
import http

import cryptography.fernet

import twisted.web.http
import twisted.web.proxy

_CHALLENGE_PAGE = b"""
<script>window.location.replace("%s")</script>
"""

kk = b'gaQ2TTVNkwyvv3Nd0Q9sm9OIk449mOwflbboCjeMk-c='
fkey = cryptography.fernet.Fernet(kk)


class NaiveReverseProxyRequest(twisted.web.http.Request):

    proxyClientFactoryClass = twisted.web.proxy.ProxyClientFactory

    def __init__(
            self, channel,
            queued=twisted.web.http._QUEUED_SENTINEL,
            reactor=twisted.internet.reactor):
        twisted.web.http.Request.__init__(self, channel, queued)
        self.reactor = reactor

    def process(self):

        def setk(cookie):
            self.addCookie(b'TWARFSESSIONID', cookie)
            self.redirect(self.uri)  # FIXME: 307 temporary redirect
            self.finish()

        def challenge(*args):
            deferred = self.channel.factory.session.put(session_id, 1)
            deferred.addCallback(challenge2)

        def challenge2(*args):
            session_id = self.received_cookies.get(b'TWARFSESSIONID')
            xxx = fkey.encrypt(session_id)
            self.write(_CHALLENGE_PAGE % xxx)
            self.finish()

        def redirect(*args):
            referer = self.getHeader(b'referer')
            self.redirect(referer)
            self.finish()

        def unchallenge(*args):
            try:
                fkey.decrypt(self.uri[1:])
            except Exception:
                challenge()
            else:
                deferred = self.channel.factory.session.put(session_id, 2)
                deferred.addCallback(redirect)

        def forward(*args):
            self.requestHeaders.setRawHeaders(
                b"host",
                [self.channel.factory.host.encode('ascii')]
            )
            clientFactory = self.proxyClientFactoryClass(
                self.method, self.uri, self.clientproto, self.getAllHeaders(),
                self.content.read(), self
            )
            self.reactor.connectTCP(
                self.channel.factory.host,
                self.channel.factory.port,
                clientFactory
            )

        def proc(bitmask):
            if bitmask == 2:
                forward()
            elif bitmask == 1:
                unchallenge()
            else:
                challenge()

        def reset(*args):
            deferred = self.channel.factory.session.new()
            deferred.addCallback(setk)

        session_id = self.received_cookies.get(b'TWARFSESSIONID')
        if not session_id:
            reset()
        else:
            deferred = self.channel.factory.session.get(session_id)
            deferred.addCallback(proc)
            deferred.addErrback(reset)
