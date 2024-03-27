from fastapi import status, APIRouter, Depends, HTTPException, UploadFile, File, Response
from fastapi.security.api_key import APIKey
from typing import Union
from pydantic import NonNegativeInt
from app.auth import service as auth
from app.modules.factory import schemas, service
from app.database import get_db, MongoSession
from app.core.schemas import ResponseStatus, BaseResponse, BaseErrorResponse

router = APIRouter(
    prefix="/v1/factories",
    tags=['Factory']
)


@router.get("/",
            description="Endpoint to fetch all the factory data",
            response_model=schemas.GetAllFactoriesResponse,
            response_model_exclude_none=True)
def get_all_factory_data(session: MongoSession = Depends(get_db),
                         index: NonNegativeInt = 1, entries: NonNegativeInt = 25):
    return service.get_all_factory_data(session.factory, index, entries)


@router.get("/{factory_id}",
            description="Endpoint to fetch a single entry of the factory document by its id",
            response_model=Union[schemas.GetFactoryResponse, BaseErrorResponse],
            response_model_exclude_none=True,
            responses={
                404: {'model': BaseErrorResponse},
                422: {'model': BaseErrorResponse}
            })
def get_factory_data_by_id(factory_id: str,
                           session: MongoSession = Depends(get_db),
                           response: Response = Response()):
    try:
        res = service.get_factory_data_by_id(session.factory, factory_id)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseErrorResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             description="Endpoint to register a new entry in the factory document",
             response_model=Union[schemas.RegisterFactoryResponse, BaseErrorResponse],
             response_model_exclude_none=True,
             responses={
                 400: {'model': BaseErrorResponse}
             })
def register_factory(request: schemas.RegisterFactoryRequest,
                     session: MongoSession = Depends(get_db),
                     api_key: APIKey = Depends(auth.get_api_key),
                     response: Response = Response()):
    try:
        res = service.register_factory(session.factory, factory=request)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseErrorResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res


@router.post("/upload",
             status_code=status.HTTP_201_CREATED,
             description="Endpoint to parse and register entries from a json file to the factory document",
             response_model=Union[schemas.UploadFactoryFileResponse, BaseErrorResponse],
             response_model_exclude_none=True,
             responses={
                 400: {'model': BaseErrorResponse},
                 404: {'model': BaseErrorResponse},
                 422: {'model': BaseErrorResponse}
             })
def upload_factory_data_file(document: UploadFile = File(...),
                             session: MongoSession = Depends(get_db),
                             api_key: APIKey = Depends(auth.get_api_key),
                             response: Response = Response()):
    try:
        res = service.upload_factory_data_file(session.factory, factory_data_file=document)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res
