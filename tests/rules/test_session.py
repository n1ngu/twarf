
import unittest.mock
import aiounittest

import twarf.proxy

from twarf.rules.session import COOKIE
from twarf.rules.session import MatchCookie


# TODO: SetCookietTest (request.temporary_redirect is a
# TwarfRequest-only feature)


class MatchCookieTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        session_srv = unittest.mock.Mock(**{
            'get.return_value': aiounittest.futurized(b'session_state')
        })
        channel = unittest.mock.Mock()
        request = twarf.proxy.TwarfRequest(channel)
        request.received_cookies[COOKIE] = b'cookie_value'

        self.assertTrue(
            await MatchCookie(session_srv, b'session_state')(request)
        )
        session_srv.get.assert_called_with(b'cookie_value')
        self.assertFalse(
            await MatchCookie(session_srv, b'another_state')(request)
        )
