
import logging

import twarf.service.logging

from . import TwarfRule
from .forward import Forward


class LogRequest(TwarfRule):

    def __init__(self, fwd, service):
        self.fwd = fwd
        self.service = service

    async def __call__(self, request):
        await self.service.log('%s', request)
        await self.fwd(request)


# TODO: log response


def twarf_rules(reactor) -> TwarfRule:

    logging_srv = twarf.service.logging.LoggingService(
        logging.getLogger('twarf')
    )

    return LogRequest(
        Forward(reactor),
        logging_srv
    )
