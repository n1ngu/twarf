
from unittest.mock import Mock
from aiounittest import AsyncTestCase
from aiounittest import futurized

from twarf.rules import TwarfRule
from twarf.rules import True_
from twarf.rules import False_
from twarf.rules import Yes
from twarf.rules import Not
from twarf.rules import And
from twarf.rules import Or


class BoolTest(AsyncTestCase):

    async def test_true(self):
        request = Mock()
        self.assertTrue(
            await True_()(request)
        )

    async def test_false(self):
        request = Mock()
        self.assertFalse(
            await False_()(request)
        )


class YesTest(AsyncTestCase):

    async def test_true(self):

        a = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await Yes(a)(request)
        )

        a.assert_called_once_with(request)

    async def test_false(self):

        a = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await Yes(a)(request)
        )

        a.assert_called_once_with(request)


class NotTest(AsyncTestCase):

    async def test_true(self):

        a = Mock(return_value=futurized(True))
        request = Mock()

        self.assertFalse(
            await Not(a)(request)
        )

        a.assert_called_once_with(request)

    async def test_false(self):

        a = Mock(return_value=futurized(False))
        request = Mock()

        self.assertTrue(
            await Not(a)(request)
        )

        a.assert_called_once_with(request)


class AndTest(AsyncTestCase):

    async def test_true_true(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await And(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_true_false(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await And(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_false_true(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertFalse(
            await And(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_false_false(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await And(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()


class OrTest(AsyncTestCase):

    async def test_true_true(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await Or(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_true_false(self):

        a = Mock(return_value=futurized(True))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertTrue(
            await Or(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_not_called()

    async def test_false_true(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(True))
        request = Mock()

        self.assertTrue(
            await Or(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)

    async def test_false_false(self):

        a = Mock(return_value=futurized(False))
        b = Mock(return_value=futurized(False))
        request = Mock()

        self.assertFalse(
            await Or(a, b)(request)
        )

        a.assert_called_once_with(request)
        b.assert_called_once_with(request)
