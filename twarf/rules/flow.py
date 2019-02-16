
from . import TwarfRule
from .http import InternalServerError


class If(TwarfRule):

    def __init__(self, test, then, orelse):
        self.test = test
        self.then = then
        self.orelse = orelse

    async def __call__(self, request):
        if await self.test(request):
            await self.then(request)
        else:
            await self.orelse(request)


class Unreachable(InternalServerError):

    async def __call__(self, request):
        # FIXME: issue warning through logging service
        print("FATAL: request reached unreachable rule")
        await super().__call__(request)
