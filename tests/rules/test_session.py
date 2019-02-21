
import unittest.mock
import aiounittest

import twarf.proxy

from twarf.rules.session import COOKIE
from twarf.rules.session import SetCookie
from twarf.rules.session import MatchCookie


class SetCookieTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        session_srv = unittest.mock.Mock(**{
            'new.return_value': aiounittest.futurized(b'new_cookie')
        })
        channel = unittest.mock.Mock()
        request = twarf.proxy.TwarfRequest(channel)

        await SetCookie(session_srv, b'default_state')(request)

        session_srv.new.assert_called_with(b'default_state')
        self.assertEqual(
            request.cookies,
            [COOKIE + b'=new_cookie']
        )


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
