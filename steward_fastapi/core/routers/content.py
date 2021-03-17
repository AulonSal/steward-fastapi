# from enum import Enum
# from typing import Optional
from fastapi import APIRouter, Depends

import steward_fastapi.core.models.database as db
import steward_fastapi.core.models.validation as data
from steward_fastapi.core.authentication import oauth2_scheme

router = APIRouter()

@router.post("/type", response_model=data.ContentType)
async def add_type(type_: data.ContentTypeIn, token: str = Depends(oauth2_scheme)):
    type_in_db = await db.ContentType.create(**type_.dict())
    return await data.ContentType.from_tortoise_orm(type_in_db)

@router.post("/source", response_model=data.ContentSource)
async def add_source(source: data.ContentSourceIn, token: str = Depends(oauth2_scheme)):
    source_in_db = await db.ContentSource.create(**source.dict())
    return await data.ContentSource.from_tortoise_orm(source_in_db)

#TODO: Refine this, check what a pydantic constructor does
@router.post("/", response_model=data.Content)
async def add_content(content: data.ContentIn, token: str = Depends(oauth2_scheme)):
    print(content)
    new_content = { k: v for k, v in content.dict().items() if 'id' not in k}
    new_content['type'] = await db.ContentType.get_or_create(name=content.dict()['type_id'])
    new_content['source'] = await db.ContentSource.get_or_create(name=content.dict()['source_id'])
    content_in_db = await db.Content.create(**content.dict())
    return await data.Content.from_tortoise_orm(content_in_db)

@router.get("/", response_model=list[data.Content])
async def get_content():
    return await data.Content.from_queryset(db.Content.all())

@router.get("/type", response_model=list[data.ContentType])
async def get_types():
    return await data.ContentType.from_queryset(db.ContentType.all())

@router.get("/source", response_model=list[data.ContentSource])
async def get_sources():
    return await data.ContentSource.from_queryset(db.ContentSource.all())

# @router.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}
#
#
# @router.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# @router.get("/items/")
# async def read_item_db(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
#
#
# @router.get("/items_str/{item_id}")
# async def read_item_string(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
