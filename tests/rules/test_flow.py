
from unittest.mock import Mock
from aiounittest import AsyncTestCase
from aiounittest import futurized

from twarf.rules.flow import If
from twarf.rules.flow import Try


class IfTest(AsyncTestCase):

    async def test_true(self):

        test = Mock(return_value=futurized(True))
        then = Mock(return_value=futurized(None))
        orelse = Mock(return_value=futurized(None))
        request = Mock()

        await If(
            test=test,
            then=then,
            orelse=orelse,
        )(request)

        test.assert_called_once_with(request)
        then.assert_called_once_with(request)
        orelse.assert_not_called()

    async def test_false(self):

        test = Mock(return_value=futurized(False))
        then = Mock(return_value=futurized(None))
        orelse = Mock(return_value=futurized(None))
        request = Mock()

        await If(
            test=test,
            then=then,
            orelse=orelse,
        )(request)

        test.assert_called_once_with(request)
        then.assert_not_called()
        orelse.assert_called_once_with(request)


class TryTest(AsyncTestCase):

    async def test_pass(self):
        request = Mock()
        body = Mock(return_value=futurized(None))
        fail = Mock(return_value=futurized(None))

        await Try(
            body=body,
            fail=fail,
        )(request)

        body.assert_called_once_with(request)
        fail.assert_not_called()

    async def test_fail(self):
        request = Mock()
        body = Mock(return_value=futurized(Exception('Dummy error')))
        fail = Mock(return_value=futurized(None))

        await Try(
            body=body,
            fail=fail,
        )(request)

        body.assert_called_once_with(request)
        fail.assert_called_once_with(request)
