
import unittest.mock
import aiounittest
import twisted.web.test.requesthelper

from twarf.rules.http import Finish
from twarf.rules.http import TempRedirect
from twarf.rules.http import Unauthorized
from twarf.rules.http import BadRequest
from twarf.rules.http import InternalServerError


class FinishTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = twisted.web.test.requesthelper.DummyRequest(b'')

        await Finish()(request)

        self.assertTrue(request.finished)
        self.assertTrue(request.responseHeaders.hasHeader(b'server'))
        self.assertTrue(request.responseHeaders.hasHeader(b'date'))


class TempRedirectTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = unittest.mock.Mock(uri=b'uri')
        await TempRedirect()(request)
        request.temporary_redirect.assert_called_once_with(b'uri')


class UnauthorizedTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = twisted.web.test.requesthelper.DummyRequest(b'')

        await Unauthorized()(request)

        self.assertEqual(request.responseCode, 401)
        self.assertTrue(request.finished)
        self.assertTrue(request.responseHeaders.hasHeader(b'server'))
        self.assertTrue(request.responseHeaders.hasHeader(b'date'))


class BadRequestTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = twisted.web.test.requesthelper.DummyRequest(b'')

        await BadRequest()(request)

        self.assertEqual(request.responseCode, 400)
        self.assertTrue(request.finished)
        self.assertTrue(request.responseHeaders.hasHeader(b'server'))
        self.assertTrue(request.responseHeaders.hasHeader(b'date'))


class InternalServerErrorTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = twisted.web.test.requesthelper.DummyRequest(b'')

        await InternalServerError()(request)

        self.assertEqual(request.responseCode, 500)
        self.assertTrue(request.finished)
        self.assertTrue(request.responseHeaders.hasHeader(b'server'))
        self.assertTrue(request.responseHeaders.hasHeader(b'date'))
