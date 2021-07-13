# from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from tortoise.exceptions import IntegrityError, DoesNotExist
from typing import Optional

import steward_fastapi.core.models.database as db
import steward_fastapi.core.models.validation as data
from steward_fastapi.core.authentication import oauth2_scheme

router = APIRouter()

@router.post("/type", response_model=data.ContentType)
async def add_type(type_: data.ContentTypeIn, token: str = Depends(oauth2_scheme)):
    type_in_db, _ = await db.ContentType.get_or_create(**type_.dict())
    return await data.ContentType.from_tortoise_orm(type_in_db)

@router.post("/source", response_model=data.ContentSource)
async def add_source(source: data.ContentSourceIn, token: str = Depends(oauth2_scheme)):
    source_in_db, _ = await db.ContentSource.get_or_create(**source.dict())
    return await data.ContentSource.from_tortoise_orm(source_in_db)

#TODO: Refine this, check what a pydantic constructor does
@router.post("/", response_model=data.Content)
async def add_content(content: data.ContentIn, token: str = Depends(oauth2_scheme)):
    print(content)
    new_content = { k: v for k, v in content.dict().items() if 'id' not in k}
    new_content['type'], _ = await db.ContentType.get_or_create(name=content.dict()['type_id'])
    new_content['source'], _ = await db.ContentSource.get_or_create(name=content.dict()['source_id'])
    try:
        content_in_db = await db.Content.create(**content.dict())
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Content Already Exists') from e
    return await data.Content.from_tortoise_orm(content_in_db)

@router.get("/", response_model=list[data.ContentOut])
async def get_content(token: str = Depends(oauth2_scheme)):
    return await data.ContentOut.from_queryset(db.Content.all())

@router.get("/type", response_model=list[data.ContentType])
async def get_types(token: str = Depends(oauth2_scheme)):
    return await data.ContentType.from_queryset(db.ContentType.all())

@router.get("/source", response_model=list[data.ContentSource])
async def get_sources(token: str = Depends(oauth2_scheme)):
    return await data.ContentSource.from_queryset(db.ContentSource.all())


@router.get("/search", response_model=list[data.ContentOut])
async def search_endpoint(string: str, type: Optional[str] = None, source: Optional[str] = None, token: str = Depends(oauth2_scheme)):
    try:
        return await data.ContentOut.from_queryset(await search_content_query(string, type, source))
    except ValueError as exception:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(exception))


# Does python not have a tool which can tell me all possible exceptions here? even just a best effort?
async def search_content_query(string: str, _type: Optional[str] = None, source: Optional[str] = None):
    try:
        if _type is not None:
            type_in_db = await db.ContentType.get(name=_type)
    except DoesNotExist:
        raise ValueError(f'''ContentType {type} does not exist''')

    try:
        if source is not None:
            source_in_db = await db.ContentSource.get(name=source)
    except DoesNotExist:
        raise ValueError(f'''ContentSource {source} does not exist''')

    query = db.Content.filter(meta__icontains=string)  # meta__search just returns everything
    if _type is not None:
        query = query.filter(type=type_in_db)
    if source is not None:
        query = query.filter(source=source_in_db)
    return query

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
