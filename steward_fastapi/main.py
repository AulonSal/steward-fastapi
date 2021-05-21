from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

import steward_fastapi.config as config
import steward_fastapi.core.routers as routers

app = FastAPI(**config.OPENAPI.dict())

register_tortoise(app=app, config=config.TORTOISE_ORM)

app.include_router(router=routers.authentication_router)
app.include_router(router=routers.content_router, prefix='/content')
app.include_router(router=routers.flexible_data_router, prefix='/flexible_data')

