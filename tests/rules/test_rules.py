
from unittest.mock import Mock
from aiounittest import AsyncTestCase
from aiounittest import futurized

from twarf.rules import True_
from twarf.rules import False_
from twarf.rules import Yes
from twarf.rules import Not


class BoolTest(AsyncTestCase):

    async def test_true(self):
        self.assertTrue(await True_()(Mock()))

    async def test_false(self):
        self.assertFalse(await False_()(Mock()))

    async def test_yes(self):
        request = Mock()
        true_ = Mock(return_value=futurized(True))
        false_ = Mock(return_value=futurized(False))

        self.assertTrue(await Yes(true_)(request))
        self.assertFalse(await Yes(false_)(request))

        true_.assert_called_once_with(request)
        false_.assert_called_once_with(request)

    async def test_not(self):
        request = Mock()
        true_ = Mock(return_value=futurized(True))
        false_ = Mock(return_value=futurized(False))

        self.assertFalse(await Not(true_)(request))
        self.assertTrue(await Not(false_)(request))

        true_.assert_called_once_with(request)
        false_.assert_called_once_with(request)

    async def test_invert(self):
        request = Mock()

        coro = Mock(return_value=futurized(True))
        test = ~Yes(coro)
        self.assertFalse(await test(request))
        coro.assert_called_once_with(request)

        coro = Mock(return_value=futurized(False))
        test = ~Yes(coro)
        self.assertTrue(await test(request))
        coro.assert_called_once_with(request)

        coro = Mock(return_value=futurized(True))
        test = ~(~Yes(coro))
        self.assertTrue(await test(request))
        coro.assert_called_once_with(request)

        coro = Mock(return_value=futurized(False))
        test = ~(~Yes(coro))
        self.assertFalse(await test(request))
        coro.assert_called_once_with(request)


class AndTest(AsyncTestCase):

    async def test_true_true(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await (Yes(a) & Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_true_false(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await (Yes(a) & Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_false_true(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertFalse(
            await (Yes(a) & Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_false_false(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await (Yes(a) & Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()


class OrTest(AsyncTestCase):

    async def test_true_true(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await (Yes(a) | Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_true_false(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertTrue(
            await (Yes(a) | Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_false_true(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await (Yes(a) | Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_false_false(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await (Yes(a) | Yes(b))(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)
