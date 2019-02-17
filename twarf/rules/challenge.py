
import twarf.service.session
import twarf.service.crypto

from . import TwarfRule
from . import TwarfTest
from .flow import If
from .http import Finish
from .forward import Forward
from .session import COOKIE
from .session import SetCookie
from .session import MatchCookie


class RedirectChallenge(Finish):

    def __init__(self,
                 next_challenge,
                 crypto_srv,
                 session_srv,
                 ):
        self.next_challenge = next_challenge
        self.crypto_srv = crypto_srv
        self.session_srv = session_srv

    async def process(self, request):
        uri = request.uri
        passed = await self.crypto_srv.decrypt(uri[1:])
        if passed and passed == b'challenge1':
            cookie = request.received_cookies.get(COOKIE)
            # FIXME: referer header might not be present, redirect to 
            # previous URI through query parameter
            referer = request.getHeader(b'referer')
            await self.session_srv.put(cookie, self.next_challenge)
            request.temporary_redirect(referer)
            await super().process(request)
        else:
            challenge = await self.crypto_srv.encrypt(b'challenge1')
            request.temporary_redirect(challenge)
            await super().process(request)


class Unchallenge(TwarfTest):

    def __init__(self, service, value):
        self.service = service
        self.value = value

    async def test(self, request):
        cookie = request.received_cookies.get(COOKIE)
        session = await self.service.get(cookie)
        return session == self.value


def twarf_rules(reactor) -> TwarfRule:

    session_srv = twarf.service.session.SessionService()
    crypto_srv = twarf.service.crypto.CryptoService([
        b'm848yHI9EE_m-PypvP8hDQvxdiMOJtw_JksWSblYHqY=',
        b'jSej64XRU1IYOZDYE62qtjdscog6HexjmjjP4M3cEoU=',
        b'L9HPLxa34i_fOWhPcPzEIzAHNYfkYChBwYIyEXVbAPs=',
    ])

    return If(
        test=MatchCookie(session_srv, b'valid'),
        then=Forward(reactor),
        orelse=If(
            test=MatchCookie(session_srv, b'challenge1'),
            then=RedirectChallenge(b'valid', crypto_srv, session_srv),
            orelse=SetCookie(session_srv, b'challenge1'),
        ),
    )
