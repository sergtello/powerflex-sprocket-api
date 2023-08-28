import pydantic as pc
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas_extensions import PydanticObjectId, make_partial_model, as_form


class SprocketBase(BaseModel):
    teeth: pc.PositiveInt
    pitch_diameter: pc.PositiveInt
    outside_diameter: pc.PositiveInt
    pitch: pc.PositiveInt


class RegisterSprocketRequest(SprocketBase):
    pass


@make_partial_model
class UpdateSprocketRequest(SprocketBase):
    pass


class StrSprocket(SprocketBase):
    id: PydanticObjectId = pc.Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChartDataBase(BaseModel):
    sprocket_production_actual: List[pc.PositiveInt]
    sprocket_production_goal: List[pc.PositiveInt]
    time: List[datetime]


class FactoryChartDataBase(BaseModel):
    chart_data: ChartDataBase


class FactoryBase(BaseModel):
    factory: FactoryChartDataBase


class RegisterFactoryRequest(FactoryBase):
    pass


class StrFactory(FactoryBase):
    id: PydanticObjectId = pc.Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
