
import unittest.mock
import twisted.trial.unittest
import twisted.test.proto_helpers

from twarf.proxy import TwarfFactory


class ProxyTest(twisted.trial.unittest.TestCase):

    def test_callback_rules(self):

        mock = unittest.mock.Mock()

        async def rules(request):
            mock(request)

        factory = TwarfFactory(rules)
        protocol = factory.buildProtocol(('127.0.0.1', 0))
        transport = twisted.test.proto_helpers.StringTransport()
        protocol.makeConnection(transport)
        protocol.dataReceived(
            b'GET / HTTP/1.1\r\n\r\n'
        )
        mock.assert_called_once_with(protocol.requests[0])
