
import asyncio


class TwarfRule():

    async def __call__(self, request):
        await asyncio.sleep(0)


class TwarfTest():

    async def __call__(self, request) -> bool:
        return await self.test(request)

    def __invert__(self):
        return Not(self)

    async def test(self, request) -> bool:
        raise NotImplementedError()


class True_(TwarfTest):

    async def test(self, request) -> bool:
        return True


class False_(TwarfTest):

    async def test(self, request) -> bool:
        return False


class Yes(TwarfTest):

    def __init__(self, a):
        self.a = a

    async def test(self, request) -> bool:
        return bool(await self.a(request))


class Not(Yes):

    async def test(self, request) -> bool:
        return not await super().test(request)


class And(TwarfTest):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    async def test(self, request) -> bool:
        return (
            await self.a(request) and await self.b(request)
        )


class Or(TwarfTest):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    async def test(self, request) -> bool:
        return (
            await self.a(request) or await self.b(request)
        )
