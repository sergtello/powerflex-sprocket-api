import pydantic as pc
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.core.schemas import BaseResponse
from app.core.schemas_extensions import PydanticObjectId, make_partial_model


class SprocketBase(BaseModel):
    teeth: pc.PositiveInt
    pitch_diameter: pc.PositiveInt
    outside_diameter: pc.PositiveInt
    pitch: pc.PositiveInt


class RegisterSprocketRequest(SprocketBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "teeth": 5,
                    "pitch_diameter": 5,
                    "outside_diameter": 6,
                    "pitch": 1
                }
            ]
        }
    }


@make_partial_model
class UpdateSprocketRequest(SprocketBase):
    pass


class StrSprocket(SprocketBase):
    id: PydanticObjectId = pc.Field(..., alias="_id")
    creation_time: datetime

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class SprocketOut(UpdateSprocketRequest):
    id: PydanticObjectId = pc.Field(..., alias="_id")
    creation_time: datetime

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class GetSprocketResponse(BaseResponse):
    data: StrSprocket

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "OK",
                    "data": {
                        "_id": str(PydanticObjectId()),
                        "creation_time": datetime.now(),
                        "teeth": 5,
                        "pitch_diameter": 5,
                        "outside_diameter": 6,
                        "pitch": 1
                    }
                }
            ]
        }
    }


class GetAllSprocketsResponse(BaseResponse):
    data: List[StrSprocket]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "OK",
                    "data": [
                        {
                            "_id": str(PydanticObjectId()),
                            "creation_time": datetime.now(),
                            "teeth": 5,
                            "pitch_diameter": 5,
                            "outside_diameter": 6,
                            "pitch": 1
                        },
                        {
                            "_id": str(PydanticObjectId()),
                            "creation_time": datetime.now(),
                            "teeth": 6,
                            "pitch_diameter": 6,
                            "outside_diameter": 7,
                            "pitch": 1
                        },

                    ]
                }
            ]
        }
    }


class RegisterSprocketResponse(GetSprocketResponse):
    pass


class UpdateSprocketResponse(BaseResponse):
    data: SprocketOut

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "OK",
                    "data": {
                        "_id": str(PydanticObjectId()),
                        "creation_time": datetime.now(),
                        "teeth": 6,
                        "pitch_diameter": 6
                    }
                }
            ]
        }
    }


class UploadSprocketFileResponse(BaseResponse):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "OK",
                    "msg": "File uploaded, 3 new sprocket entries were saved"
                }
            ]
        }
    }
