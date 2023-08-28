from fastapi import status, APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security.api_key import APIKey
from typing import List
from app import schemas, utils, auth

router = APIRouter(
    prefix="/v1/factory",
    tags=['Factory']
)


@router.get("/{factory_id}", response_model=schemas.StrFactory, response_model_exclude_none=True)
async def get_factory_data_by_id(factory_id: str):
    return utils.get_factory_data_by_id(factory_id)


@router.get("/", response_model=List[schemas.StrFactory], response_model_exclude_none=True)
async def get_all_factory_data(index: int = 1, entries: int = 25):
    return utils.get_all_factory_data(index, entries)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=List[schemas.StrFactory], response_model_exclude_none=True)
async def upload_factory_data_file(document: UploadFile = File(...), api_key: APIKey = Depends(auth.get_api_key)):
    return utils.upload_factory_data_file(factory_data_file=document)
