
import http
import hashlib
import asyncio

import twarf.service.auth

from .flow import Unauthorized
from .forward import Forward


REALM = b"Twarf"


class BasicAuth(Unauthorized):


    def __init__(self, service, fwd):
        self.service = service
        self.fwd = fwd

    async def __call__(self, request):
        
        if await self.service.auth(
                request.getUser(), request.getPassword()
                ):
            # FIXME: clean authroization credentials from the forwarded
            # request so that they dont get leaked upstream
            await self.fwd(request)
        else:
            request.setHeader(
                b"WWW-Authenticate",
                b'Basic realm="%s", charset="UTF-8"' % REALM
            )
            await super().__call__(request)


async def plain(secret:bytes):
    return secret


async def sha256x10(secret:bytes):
    hash_ = secret
    salt = b'jump!'
    for _ in range(10):
        # Ideally you'd compute the hashes in a service in a
        # separate process. Otherwise, do not forget to cooperate
        # with the other coroutines and yield execution
        # as often as possible
        await asyncio.sleep(0)
        hash_ = hashlib.sha256(hash_ + salt).hexdigest().encode()
    return hash_


def twarf_rules(reactor):

    async def secrets(user:bytes):
        # import asyncio
        # from twarf.rules.auth import sha256x10
        # loop = asyncio.get_event_loop()
        # print(loop.run_until_complete())
        return {
            b'jane': b'supersecret'
        }.get(user)

    auth_srv = twarf.service.auth.AuthSecretHashService(
        plain, secrets
    )
    return BasicAuth(
        auth_srv, Forward(reactor)
    )
