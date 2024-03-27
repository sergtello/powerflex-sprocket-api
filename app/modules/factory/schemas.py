import pydantic as pc
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from typing import Optional, List, Union
from app.core.schemas import BaseResponse
from app.core.schemas_extensions import PydanticObjectId


class ChartDataBase(BaseModel):
    sprocket_production_actual: List[pc.PositiveInt]
    sprocket_production_goal: List[pc.PositiveInt]
    time: List[datetime]


class FactoryChartDataBase(BaseModel):
    chart_data: ChartDataBase


class FactoryBase(BaseModel):
    factory: FactoryChartDataBase


class RegisterFactoryRequest(FactoryBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "factory": {
                        "chart_data": {
                          "sprocket_production_actual": [
                            32,
                            29,
                            31,
                            30,
                            32
                          ],
                          "sprocket_production_goal": [
                            32,
                            30,
                            31,
                            29,
                            32
                          ],
                          "time": [
                            1611194818,
                            1611194878,
                            1611194938,
                            1611194998,
                            1611195058
                          ]
                        }
                    }
                }
            ]
        }
    )


class StrFactory(FactoryBase):
    id: PydanticObjectId = pc.Field(..., alias="_id")
    creation_time: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True
    )


class GetFactoryResponse(BaseResponse):
    data: StrFactory

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "OK",
                    "data": {
                        "_id": str(PydanticObjectId()),
                        "creation_time": datetime.now(tz=timezone.utc),
                        "factory": {
                            "chart_data": {
                                "sprocket_production_actual": [
                                    32,
                                    29,
                                    31,
                                    30,
                                    32
                                ],
                                "sprocket_production_goal": [
                                    32,
                                    30,
                                    31,
                                    29,
                                    32
                                ],
                                "time": [
                                    1611194818,
                                    1611194878,
                                    1611194938,
                                    1611194998,
                                    1611195058
                                ]
                            }
                        }
                    }
                }
            ]
        }
    )


class GetAllFactoriesResponse(BaseResponse):
    data: List[StrFactory]

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "OK",
                    "data": [
                        {
                            "_id": str(PydanticObjectId()),
                            "creation_time": datetime.now(tz=timezone.utc),
                            "factory": {
                                "chart_data": {
                                    "sprocket_production_actual": [
                                        32,
                                        29,
                                        31,
                                        30,
                                        32
                                    ],
                                    "sprocket_production_goal": [
                                        32,
                                        30,
                                        31,
                                        29,
                                        32
                                    ],
                                    "time": [
                                        1611194818,
                                        1611194878,
                                        1611194938,
                                        1611194998,
                                        1611195058
                                    ]
                                }
                            }
                        },
                        {
                            "_id": str(PydanticObjectId()),
                            "creation_time": datetime.now(tz=timezone.utc),
                            "factory": {
                                "chart_data": {
                                    "sprocket_production_actual": [
                                        33,
                                        30,
                                        32,
                                        31,
                                        33
                                    ],
                                    "sprocket_production_goal": [
                                        33,
                                        31,
                                        32,
                                        30,
                                        33
                                    ],
                                    "time": [
                                        1611184818,
                                        1611184878,
                                        1611184938,
                                        1611184998,
                                        1611185058
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        }
    )


class RegisterFactoryResponse(GetFactoryResponse):
    pass


class UploadFactoryFileResponse(BaseResponse):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "OK",
                    "msg": "File uploaded, 3 new factory entries were saved"
                }
            ]
        }
    )

