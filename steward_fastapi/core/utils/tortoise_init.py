from tortoise import Tortoise
from steward_fastapi.config.database import CONFIG
import atexit

async def init():
    await Tortoise.init(config=CONFIG)

async def cleanup():
    await Tortoise.close_connections()

#TODO: Handle cleanup

