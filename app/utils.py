import json
from app import models as md
from app import schemas as sch
from mongoengine import queryset, errors
from fastapi import HTTPException, status, UploadFile


def get_all_factory_data(index: int, entries: int):
    return [sch.StrFactory.model_validate(factory, from_attributes=True) for factory in
            md.Factory.objects.skip(index - 1).limit(entries)]


def get_factory_data_by_id(factory_id: str):
    try:
        factory = md.Factory.objects.get(id=factory_id)
    except queryset.DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Factory {str(factory_id)} does not exist")
    except errors.ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Error fetching factory: {str(exc)}")
    else:
        return sch.StrFactory.model_validate(factory, from_attributes=True)


def register_factory(factory: sch.RegisterFactoryRequest):
    try:
        new_factory = md.Sprocket(**factory.model_dump(exclude_none=True)).save()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error registering factory, an exception occurred: {str(exc)}")
    else:
        return sch.StrFactory.model_validate(new_factory, from_attributes=True)


def upload_factory_data_file(factory_data_file: UploadFile):
    if factory_data_file.content_type != 'application/json':
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Error, only json files are supported")
    factory_data_json = json.loads(factory_data_file.file.read())
    if 'factories' not in factory_data_json.keys():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Invalid file, 'factories' key not found")
    saved_factory_data = []
    for fd in factory_data_json['factories']:
        try:
            fd_schema = sch.RegisterFactoryRequest(**fd)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error uploading factory file, an exception occurred: {str(exc)}")
        else:
            new_factory_data = md.Factory(**fd_schema.model_dump(exclude_none=True)).save()
            saved_factory_data.append(sch.StrFactory.model_validate(new_factory_data, from_attributes=True))

    return saved_factory_data


def get_all_sprockets(index: int, entries: int):
    return [sch.StrSprocket.model_validate(sprocket, from_attributes=True) for sprocket in
            md.Sprocket.objects.skip(index - 1).limit(entries)]


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
        return sch.StrSprocket.model_validate(sprocket, from_attributes=True)


def register_sprocket(sprocket: sch.RegisterSprocketRequest):
    try:
        new_sprocket = md.Sprocket(**sprocket.model_dump(exclude_none=True)).save()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error registering sprocket, an exception occurred: {str(exc)}")
    else:
        return sch.StrSprocket.model_validate(new_sprocket, from_attributes=True)


def update_sprocket(sprocket_id: str, sprocket: sch.UpdateSprocketRequest):
    try:
        get_sprocket_by_id(sprocket_id)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code,detail=f"{exc.detail}")
    else:
        fields_sprocket = sprocket.model_dump(exclude_none=True, exclude_unset=True)
        if not fields_sprocket:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f"Error updating sprocket {sprocket_id}, no fields were provided")
        else:
            updated_sprocket = md.Sprocket.objects(id=sprocket_id).modify(**fields_sprocket, new=True)
            return sch.StrSprocket.model_validate(updated_sprocket, from_attributes=True)


def upload_sprocket_file(sprocket_file: UploadFile):
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error uploading sprocket file, an exception occurred: {str(exc)}")
        else:
            new_sprocket = md.Sprocket(**sp_schema.model_dump(exclude_none=True)).save()
            saved_sprockets.append(sch.StrSprocket.model_validate(new_sprocket, from_attributes=True))

    return saved_sprockets
