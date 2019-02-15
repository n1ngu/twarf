
import twarf.proxy


class Twarf():

    def __init__(
            self,
            options,
            reactor):
        self.options = options
        self.reactor = reactor
        print('Listening on port %d' % self.options.port)
        self.reactor.listenTCP(
            self.options.port,
            twarf.proxy.TwarfFactory(
                self.options.rules,
                self.reactor
            )
        )
    
    def run(self):
        self.reactor.run()

