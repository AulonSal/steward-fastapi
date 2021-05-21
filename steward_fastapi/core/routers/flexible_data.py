from fastapi import APIRouter, Depends

import steward_fastapi.core.models.database as db
import steward_fastapi.core.models.validation as data
from steward_fastapi.core.authentication import oauth2_scheme

router = APIRouter()

@router.post("/", response_model=data.FlexibleData)
async def add_flexible_data(flexible_data: data.FlexibleData, token: str = Depends(oauth2_scheme)):
    flexible_data_in_db, _ = await db.ContentType.get_or_create(**flexible_data.dict())
    return await data.FlexibleData.from_tortoise_orm(flexible_data_in_db)

@router.get("/", response_model=list[data.ContentType])
async def get_flexible_data(token: str = Depends(oauth2_scheme)):
    return await data.FlexibleData.from_queryset(db.FlexibleData.all())

