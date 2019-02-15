
import importlib

import twarf.proxy


class Twarf():

    def __init__(self, options, reactor):

        self.reactor = reactor

        rules_module = importlib.import_module(options.rules)
        rules = rules_module.twarf_rules(reactor)

        print('Listening on port %d' % options.port)
        self.reactor.listenTCP(
            options.port,
            twarf.proxy.TwarfFactory(rules)
        )
    
    def run(self):
        self.reactor.run()

