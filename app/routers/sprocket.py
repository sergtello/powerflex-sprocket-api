from fastapi import status, APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.security.api_key import APIKey
from typing import List, Annotated
from app import schemas, utils, auth

router = APIRouter(
    prefix="/v1/sprocket",
    tags=['Sprocket']
)


@router.get("/{sprocket_id}", response_model=schemas.StrSprocket, response_model_exclude_none=True)
async def get_sprocket_by_id(sprocket_id: str):
    return utils.get_sprocket_by_id(sprocket_id)


@router.get("/", response_model=List[schemas.StrSprocket], response_model_exclude_none=True)
async def get_all_sprockets(index: int = 1, entries: int = 25):
    return utils.get_all_sprockets(index, entries)


@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=List[schemas.StrSprocket], response_model_exclude_none=True)
async def upload_sprocket_file(document: UploadFile = File(...), api_key: APIKey = Depends(auth.get_api_key)):
    return utils.upload_sprocket_file(sprocket_file=document)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.StrSprocket, response_model_exclude_none=True)
async def register_sprocket(request: schemas.RegisterSprocketRequest, api_key: APIKey = Depends(auth.get_api_key)):
    return utils.register_sprocket(sprocket=request)


@router.put("/{sprocket_id}", response_model=schemas.StrSprocket, response_model_exclude_none=True)
async def update_sprocket(sprocket_id: str, request: schemas.UpdateSprocketRequest, api_key: APIKey = Depends(auth.get_api_key)):
    return utils.update_sprocket(sprocket_id, request)
