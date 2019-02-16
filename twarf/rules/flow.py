
class If():

    def __init__(self, test, then, orelse):
        self.test = test
        self.then = then
        self.orelse = orelse

    async def process(self, request):
        if await self.test.process(request):
            await self.then.process(request)
        else:
            await self.orelse.process(request)
