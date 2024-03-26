import json
from app.modules.sprocket import models as md
from app.modules.sprocket import schemas as sch
from app.core.schemas import BaseResponse, ResponseStatus
from mongoengine import queryset, errors
from fastapi import HTTPException, status, UploadFile


def get_all_sprockets(index: int, entries: int):
    sprocket_data = [sch.StrSprocket.model_validate(sprocket, from_attributes=True) for sprocket in
                     md.Sprocket.objects.skip(index - 1).limit(entries)]
    return sch.GetAllSprocketsResponse(
        status=ResponseStatus.OK,
        msg=None,
        data=sprocket_data
    )

def get_sprocket_by_id(sprocket_id: str):
    try:
        sprocket = md.Sprocket.objects.get(id=sprocket_id)
    except queryset.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Sprocket {str(sprocket_id)} does not exist")
    except errors.ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Error fetching sprocket: {str(exc)}")
    else:
        return sch.GetSprocketResponse(
            status=ResponseStatus.OK,
            msg=None,
            data=sch.StrSprocket.model_validate(sprocket, from_attributes=True)
        )


def register_sprocket(sprocket: sch.RegisterSprocketRequest):
    try:
        new_sprocket = md.Sprocket(**sprocket.model_dump(exclude_none=True)).save()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error registering sprocket, an exception occurred: {str(exc)}")
    else:
        return sch.RegisterSprocketResponse(
            status=ResponseStatus.OK,
            msg=None,
            data=sch.StrSprocket.model_validate(new_sprocket, from_attributes=True)
        )


def update_sprocket(sprocket_id: str, sprocket: sch.UpdateSprocketRequest):
    try:
        get_sprocket_by_id(sprocket_id)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=f"{exc.detail}")
    else:
        fields_sprocket = sprocket.model_dump(exclude_none=True, exclude_unset=True)
        if not fields_sprocket:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Error updating sprocket {sprocket_id}, no fields were provided")
        else:
            updated_sprocket = md.Sprocket.objects(id=sprocket_id).modify(**fields_sprocket, new=True)
            return sch.UpdateSprocketResponse(
                status=ResponseStatus.OK,
                data=sch.SprocketOut.model_validate(updated_sprocket, from_attributes=True)
            )


def upload_sprocket_file(sprocket_file: UploadFile):
    if sprocket_file.content_type is not None:
        if sprocket_file.content_type != 'application/json':
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Error, only json files are supported")
    sprockets_json = json.loads(sprocket_file.file.read())
    if 'sprockets' not in sprockets_json.keys():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid file, sprockets key not found")
    saved_sprockets = []
    for sp in sprockets_json['sprockets']:
        try:
            sp_schema = sch.RegisterSprocketRequest(**sp)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Error uploading sprocket file, an exception occurred: {str(exc)}")
        else:
            new_sprocket = md.Sprocket(**sp_schema.model_dump(exclude_none=True)).save()
            saved_sprockets.append(sch.StrSprocket.model_validate(new_sprocket, from_attributes=True))

    return sch.UploadSprocketFileResponse(
        status=ResponseStatus.OK,
        msg=f"File uploaded, {len(saved_sprockets)} new sprocket entries were saved"
    )
