from fastapi import status, APIRouter, Depends, UploadFile, File, Response, HTTPException
from fastapi.security.api_key import APIKey
from typing import Union
from pydantic import NonNegativeInt
from app.auth import service as auth
from app.modules.sprocket import schemas, service
from app.database import get_db, MongoSession
from app.core.schemas import ResponseStatus, BaseResponse, BaseErrorResponse

router = APIRouter(
    prefix="/v1/sprockets",
    tags=['Sprocket']
)


@router.get("/",
            description="Endpoint to fetch all the sprocket data",
            response_model=schemas.GetAllSprocketsResponse,
            response_model_exclude_none=True)
def get_all_sprockets(session: MongoSession = Depends(get_db),
                      index: NonNegativeInt = 1, entries: NonNegativeInt = 25):
    return service.get_all_sprockets(session.sprocket, index, entries)


@router.get("/{sprocket_id}",
            description="Endpoint to fetch a single entry of the sprocket document",
            response_model=Union[schemas.GetSprocketResponse, BaseErrorResponse],
            response_model_exclude_none=True,
            responses={
                404: {'model': BaseErrorResponse},
                422: {'model': BaseErrorResponse}
            })
def get_sprocket_by_id(sprocket_id: str,
                       session: MongoSession = Depends(get_db),
                       response: Response = Response()):
    try:
        res = service.get_sprocket_by_id(session.sprocket, sprocket_id)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseErrorResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res


@router.post("/", status_code=status.HTTP_201_CREATED,
             description="Endpoint to register a new entry in the sprocket document",
             response_model=Union[schemas.RegisterSprocketResponse, BaseErrorResponse],
             response_model_exclude_none=True,
             responses={
                 400: {'model': BaseErrorResponse}
             })
def register_sprocket(request: schemas.RegisterSprocketRequest,
                      session: MongoSession = Depends(get_db),
                      api_key: APIKey = Depends(auth.get_api_key),
                      response: Response = Response()):
    try:
        res = service.register_sprocket(session.sprocket, request)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseErrorResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res


@router.patch("/{sprocket_id}",
              description="Endpoint to update some fields from an specific entry of the sprocket document",
              response_model=Union[schemas.UpdateSprocketResponse, BaseErrorResponse],
              response_model_exclude_none=True,
              responses={
                  404: {'model': BaseErrorResponse},
                  422: {'model': BaseErrorResponse}
              })
def update_sprocket(sprocket_id: str,
                    request: schemas.UpdateSprocketRequest,
                    session: MongoSession = Depends(get_db),
                    api_key: APIKey = Depends(auth.get_api_key),
                    response: Response = Response()):
    try:
        res = service.update_sprocket(session.sprocket, sprocket_id, request)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseErrorResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res


@router.post("/upload",
             status_code=status.HTTP_201_CREATED,
             description="Endpoint to parse and register entries from a json file to the sprocket document",
             response_model=Union[schemas.UploadSprocketFileResponse, BaseErrorResponse],
             response_model_exclude_none=True,
             responses={
                 400: {'model': BaseErrorResponse},
                 404: {'model': BaseErrorResponse},
                 422: {'model': BaseErrorResponse}
             })
def upload_sprocket_file(document: UploadFile = File(...),
                         session: MongoSession = Depends(get_db),
                         api_key: APIKey = Depends(auth.get_api_key),
                         response: Response = Response()):
    try:
        res = service.upload_sprocket_file(session.sprocket, sprocket_file=document)
    except HTTPException as e:
        response.status_code = e.status_code
        return BaseResponse(status=ResponseStatus.ERROR, msg=e.detail)
    else:
        return res
