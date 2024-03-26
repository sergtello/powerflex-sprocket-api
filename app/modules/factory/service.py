import json
from app.modules.factory import models as md
from app.modules.factory import schemas as sch
from app.core.schemas import BaseResponse, ResponseStatus
from mongoengine import queryset, errors
from fastapi import HTTPException, status, UploadFile


def get_all_factory_data(index: int, entries: int):
    factory_data = [sch.StrFactory.model_validate(factory, from_attributes=True) for factory in
                    md.Factory.objects.skip(index - 1).limit(entries)]
    return sch.GetAllFactoriesResponse(
        status=ResponseStatus.OK,
        msg=None,
        data=factory_data
    )


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
        return sch.GetFactoryResponse(
            status=ResponseStatus.OK,
            msg=None,
            data=sch.StrFactory.model_validate(factory, from_attributes=True)
        )


def register_factory(factory: sch.RegisterFactoryRequest):
    try:
        new_factory = md.Factory(**factory.model_dump(exclude_none=True)).save()
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error registering factory, an exception occurred: {str(exc)}")
    else:
        return sch.RegisterFactoryResponse(
            status=ResponseStatus.OK,
            msg=None,
            data=sch.StrFactory.model_validate(new_factory, from_attributes=True)
        )


def upload_factory_data_file(factory_data_file: UploadFile):
    if factory_data_file.content_type is not None:
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
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Error uploading factory file, an exception occurred: {str(exc)}")
        else:
            new_factory_data = md.Factory(**fd_schema.model_dump(exclude_none=True)).save()
            saved_factory_data.append(sch.StrFactory.model_validate(new_factory_data, from_attributes=True))

    return sch.UploadFactoryFileResponse(
        status=ResponseStatus.OK,
        msg=f"File uploaded, {len(saved_factory_data)} new factory entries were saved"
    )
