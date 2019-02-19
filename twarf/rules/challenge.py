
import urllib.parse

import twarf.service.session
import twarf.service.crypto
import twarf._utils

from .flow import If
from .http import Finish
from .forward import Forward
from .session import COOKIE
from .session import SetCookie
from .session import MatchCookie


class _RedirectChallenge(Finish):

    REF = b'referer'

    def __init__(self,
                 next_challenge,
                 crypto_srv,
                 session_srv,
                 ):
        self.next_challenge = next_challenge
        self.crypto_srv = crypto_srv
        self.session_srv = session_srv
        self.secret = twarf._utils.build_random_string()

    async def process(self, request):
        uri = urllib.parse.urlparse(
            request.uri
        )
        passed = await self.crypto_srv.decrypt(uri.path[1:])
        if passed and passed == self.secret:
            cookie = request.received_cookies.get(COOKIE)
            await self.session_srv.put(cookie, self.next_challenge)
            query = urllib.parse.parse_qs(uri.query)
            quoted_referers = query.get(self.REF)
            if not quoted_referers:
                raise NotImplementedError("")  # TODO: 400 BadRequest
            referer = urllib.parse.unquote_to_bytes(quoted_referers[0])
            request.temporary_redirect(referer)
        else:
            challenge = await self.crypto_srv.encrypt(self.secret)
            referer = urllib.parse.quote_from_bytes(request.uri).encode()
            query = urllib.parse.urlencode({self.REF: referer}).encode()
            location = urllib.parse.urlunparse(
                (None, None, challenge, None, query, None)
            )
            await self.challenge(request, location)

        await super().process(request)

    async def challenge(self, request, location: bytes):
        raise NotImplementedError("")


class RedirectChallenge(_RedirectChallenge):
    """
    Redirect through a 307 response

    Drawbacks:
      - Easily spoofable
    """

    async def challenge(self, request, location: bytes):
        request.temporary_redirect(location)


class _HtmlTemplateChallenge(_RedirectChallenge):
    """
    Redirect through a page with a <meta http-equiv="refresh"/> html tag

    Drawbacks:
      - If it happens too often users might get stuck on pages, unable
        to navigate backwards
      - Original requests won't be replayed (POST, PUT, ...)
    """

    TPL = b''

    async def challenge(self, request, location: bytes):
        # FIXME: prevent downstream from caching this page
        page = self.TPL % location
        request.write(page)


class MetaRedirectChallenge(_HtmlTemplateChallenge):
    """
    Redirect through a page with a <meta http-equiv="refresh"/> html tag

    Drawbacks:
      - If it happens too often users might get stuck on pages, unable
        to navigate backwards
      - Original requests won't be replayed (POST, PUT, ...)
    """

    TPL = b"""
    <meta http-equiv="refresh" content="0; url=%s" />
    """


class JsRedirectChallenge(_HtmlTemplateChallenge):
    """
    Redirect through a page with javascript

    Drawbacks:
      - If it happens too often users might get stuck on pages, unable
        to navigate backwards
      - Original requests won't be replayed (POST, PUT, ...)
      - Won't work without javascript
    """

    TPL = b"""
    <script>window.location.replace("%s")</script>
    """


# TODO: js payload challenge
# TODO: captchas!


def twarf_rules(reactor):

    session_srv = twarf.service.session.SessionService()
    crypto_srv = twarf.service.crypto.CryptoService([
        # FIXME load from file stated in environ vars / options
        b'm848yHI9EE_m-PypvP8hDQvxdiMOJtw_JksWSblYHqY=',
        b'jSej64XRU1IYOZDYE62qtjdscog6HexjmjjP4M3cEoU=',
        b'L9HPLxa34i_fOWhPcPzEIzAHNYfkYChBwYIyEXVbAPs=',
    ])

    return If(
        test=MatchCookie(session_srv, b'valid'),
        then=Forward(reactor),
        orelse=If(
            test=MatchCookie(session_srv, b'x3'),
            then=JsRedirectChallenge(b'valid', crypto_srv, session_srv),
            orelse=If(
                test=MatchCookie(session_srv, b'x2'),
                then=MetaRedirectChallenge(b'x3', crypto_srv, session_srv),
                orelse=If(
                    test=MatchCookie(session_srv, b'x1'),
                    then=RedirectChallenge(b'x2', crypto_srv, session_srv),
                    orelse=SetCookie(session_srv, b'x1'),
                ),
            ),
        ),
    )
