import asyncio

import uvicorn
from tortoise import Tortoise, run_async

from main import app

# Uvicorn does not expose a run_from_config to go along with uvicorn.config
CONFIG = dict(
        app='main:app',  # app must be passed using import string to enable reload or workers
        host='localhost',
        port=8000,
        log_level='info',
        reload=True,
    )

if __name__ == '__main__':
    uvicorn.run(**CONFIG)
    run_async(Tortoise.close_connections())

