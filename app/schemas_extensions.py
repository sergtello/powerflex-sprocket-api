import inspect
from fastapi import Form
from pydantic.fields import FieldInfo
from pydantic import BaseModel, create_model
from bson.objectid import ObjectId as BsonObjectId
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from copy import deepcopy
from typing import Optional, Type, TypeVar, Any, Annotated, Tuple


def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
    new = deepcopy(field)
    new.default = default
    new.annotation = Optional[field.annotation]  # type: ignore
    return new.annotation, new


BaseModelT = TypeVar('BaseModelT', bound=BaseModel)


def make_partial_model(model: Type[BaseModelT]) -> Type[BaseModelT]:
    return create_model(  # type: ignore
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.model_fields.items()
        }
    )


class ObjectIdPydanticAnnotation:
    @classmethod
    def validate_object_id(cls, v: Any, handler) -> BsonObjectId:
        if isinstance(v, BsonObjectId):
            return v

        s = handler(v)
        if BsonObjectId.is_valid(s):
            return BsonObjectId(s)
        else:
            raise ValueError("Invalid ObjectId")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, _handler) -> core_schema.CoreSchema:
        assert source_type is BsonObjectId
        return core_schema.no_info_wrap_validator_function(
            cls.validate_object_id,
            core_schema.str_schema(),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler) -> JsonSchemaValue:
        return handler(core_schema.str_schema())


PydanticObjectId = Annotated[BsonObjectId, ObjectIdPydanticAnnotation]


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.model_fields.items():
        model_field: FieldInfo  # type: ignore

        new_parameters.append(
             inspect.Parameter(
                 model_field.alias,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.is_required() else Form(model_field.default),
                 annotation=model_field.annotation,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls
