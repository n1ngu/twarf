
import os
import asyncio

import molotov


TARGET = os.environ['MOLOTOV_TARGET']
TIMEOUT = float(os.environ['MOLOTOV_TIMEOUT'])


@molotov.scenario()
async def scenario_index(session):
    await asyncio.wait_for(_probe_index(session), TIMEOUT)


async def _probe_index(session):
    async with session.get(TARGET) as resp:
        assert resp.status == 200
