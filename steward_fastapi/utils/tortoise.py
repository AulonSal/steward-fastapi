import atexit
from functools import wraps

from tortoise import Tortoise

from steward_fastapi.config.database import CONFIG


# Really these two are for ipython
# TODO: Handle cleanup
async def init():
    await Tortoise.init(config=CONFIG)

async def cleanup():
    await Tortoise.close_connections()
    
class TortoiseContext:
    async def __aenter__(self):
        await Tortoise.init(config=CONFIG)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await Tortoise.close_connections()

    # Copied from https://github.com/python/cpython/blob/master/Lib/contextlib.py#L86
    def _recreate_cm(self):
        """Return a recreated instance of self."""
        return self

    def __call__(self, func):
        @wraps(func)
        async def inner(*args, **kwds):
            async with self._recreate_cm():
                return await func(*args, **kwds)

        return inner

