
import urllib.parse

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
        uri = urllib.parse.urlparse(
            request.uri
        )
        passed = await self.crypto_srv.decrypt(uri.path[1:])
        if passed and passed == b'challenge1':
            cookie = request.received_cookies.get(COOKIE)
            query = urllib.parse.parse_qs(uri.query)
            quoted_referers = query.get(b'referer')
            if not quoted_referers:
                raise NotImplementedError("")  # TODO: 400 BadRequest
            referer = urllib.parse.unquote_to_bytes(quoted_referers[0])
            await self.session_srv.put(cookie, self.next_challenge)
            request.temporary_redirect(referer)
            await super().process(request)
        else:
            challenge = await self.crypto_srv.encrypt(b'challenge1')
            referer = urllib.parse.quote_from_bytes(request.uri).encode()
            query = urllib.parse.urlencode({b'referer': referer}).encode()
            location = urllib.parse.urlunparse(
                (None, None, challenge, None, query, None)
            )
            request.temporary_redirect(location)
            await super().process(request)


# TODO: html meta redirect challenge
# TODO: js redirect challenge
# TODO: js payload challenge
# TODO: captchas!


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
