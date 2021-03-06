
from . import TwarfRule
from . import TwarfTest
from .http import InternalServerError


class If(TwarfRule):

    def __init__(self, test: TwarfTest, then: TwarfRule, orelse: TwarfRule):
        self.test = test
        self.then = then
        self.orelse = orelse

    async def process(self, request):
        if await self.test(request):
            await self.then(request)
        else:
            await self.orelse(request)


class Try(TwarfRule):

    def __init__(self, body: TwarfTest, fail: TwarfRule):
        self.body = body
        self.fail = fail

    async def process(self, request):
        try:
            await self.body(request)
        except Exception:
            await self.fail(request)


class Unreachable(InternalServerError):

    async def process(self, request):
        # FIXME: issue warning through logging service
        print("FATAL: request reached unreachable rule")
        await super().process(request)
