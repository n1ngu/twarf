
class ListService():

    # FIXME: I am synchronous!

    def __init__(self):
        self.list = set()  # You know what I mean

    async def add(self, key):
        self.list.add(key)

    async def discard(self, key):
        self.list.discard(key)

    async def clear(self):
        self.list.clear()

    async def update(self, list_: set):
        self.list.update(list_)

    async def contains(self, key) -> bool:
        return key in self.list
