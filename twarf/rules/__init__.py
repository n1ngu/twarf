
import asyncio


class TwarfRule():

    async def __call__(self, request):
        await asyncio.sleep(0)
