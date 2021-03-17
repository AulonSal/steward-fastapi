import trio_asyncio
import uvicorn

from .main import app
from .run_uvicorn import CONFIG

if __name__ == "__main__":
    config = uvicorn.Config(**CONFIG)
    server = uvicorn.Server(config=config)
    trio_asyncio.run(trio_asyncio.aio_as_trio(server.serve))

