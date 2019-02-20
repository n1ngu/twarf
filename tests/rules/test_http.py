
import aiounittest
import twisted.web.test.requesthelper

from twarf.rules.http import Finish, BadRequest


class FinishTest(aiounittest.AsyncTestCase):

    async def test_rule(self):
        request = twisted.web.test.requesthelper.DummyRequest(b'')

        await Finish()(request)

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
