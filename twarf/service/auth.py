
class AuthSecretHashService():

    def __init__(self, hash_f, hash_list):
        self.hash_f = hash_f
        self.hash_list = hash_list

    async def auth(self, user:bytes, secret:bytes) -> bool:
        hash_ = await self.hash_list(user)
        return hash_ and (hash_ == await self.hash_f(secret))

