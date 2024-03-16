# from typing import Optional, Any, Type
#
# from pydantic import BaseModel, PositiveInt, AnyUrl, Field
#
#
# class BasePaginator(BaseModel):
#     count: PositiveInt
#     next: Optional[AnyUrl] = Field(default=None)
#     prev: Optional[AnyUrl] = Field(default=None)
#     result: list[Any]
#
#
# class Paginator(object):
#
#     def __class_getitem__(cls, schema: Type[BaseModel]) -> Type[BasePaginator]:
#         return type(    # noqa
#             f"{schema.__name__}Paginator",
#             (BasePaginator, ),
#             {
#                 "__anotations__": {
#                     "result": list[schema]
#                 }
#             }
#         )
