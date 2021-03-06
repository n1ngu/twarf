
import twarf.service.list

from . import TwarfRule
from . import TwarfTest
from .flow import If
from .forward import Forward
from .forward import Throttle


class IPList(TwarfTest):

    def __init__(self, service):
        self.service = service

    async def test(self, request) -> bool:
        return await self.service.contains(
            request.getClientIP()
        )


def twarf_rules(reactor) -> TwarfRule:

    white_list = twarf.service.list.ListService()
    red_list = twarf.service.list.ListService()
    # DONT: black_list. Black lists are THE anti-DOS pitfall

    forward = Forward(reactor)
    challenge = forward  # TODO: real challenge for non-white list

    return If(
        test=IPList(white_list),
        then=forward,
        orelse=If(
            test=IPList(red_list),
            then=Throttle(forward, delay=1),
            orelse=challenge,
        ),
    )
