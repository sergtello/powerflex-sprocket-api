from pydantic import BaseModel
from enum import Enum
from typing import Optional, Union, Any


class ResponseStatus(str, Enum):
    OK = 'OK'
    ERROR = 'ERROR'


class BaseResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.OK
    msg: Optional[str] = None
    data: Optional[Union[dict, Any]] = {}


class BaseErrorResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.ERROR
    msg: str
