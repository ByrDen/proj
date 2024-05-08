from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from starlette import status

from shop import crud
from shop.models import Man
from shop.schemas import ManDetail, ManCreateForm, ManEditForm, ManDetailWithoutDepartments
from src.dependencies import DBSession

router = APIRouter(prefix="/mans",
                   tags=["Mans"])


@router.post(
    path="/",
    response_model=ManDetail,
    name="shop_man_create"
)
async def man_create(
        session: DBSession,
        data: ManCreateForm
):
    """Создание человека""" # noqa
    try:
        obj = await crud.create_man(
            session=session,
            data=data
        )
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Man {data.surname} {data.name} exist")
    else:
        return ManDetail.model_validate(obj=obj[0], from_attributes=True)


@router.get(
    path="/",
    response_model=list[ManDetail],
    name="shop_man_list"
)
async def man_list(
        session: DBSession,
        order_by: Literal["id", "name"] = Query(default="id", alias="orderBy"),
        order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection")
):
    """Получение всех людей"""
    statement = select(Man).options(selectinload(Man.departments)).order_by(
        getattr(getattr(Man, order_by), order)()
    )
    objs = await session.scalars(statement=statement)
    return [ManDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.all()]


@router.put(path="/")
async def mans_update_all(
        session: DBSession
):
    """Массовое Обновление всех людей"""
    # obj= Man()
    ...


@router.delete(path="/")
async def mans_delete_all(
        session: DBSession,
):
    """Удаление всех людей"""
    ...


@router.get(
    path='/{pk}',
    response_model=ManDetail
)
async def man_detail(
        session: DBSession,
        pk: int = Path(
            default=...,
            ge=1,
            title="Man ID",
            examples=[42]
        )
):
    """Детали про человека по id={pk} """
    obj = await crud.get_man_by_id(session=session, pk=pk)
    return ManDetail.model_validate(obj=obj, from_attributes=True)


@router.post(path='/{pk}')
async def man_create(
        pk: int = Path(
            default=...,
            ge=1,
            title="Man ID",
            examples=[42]
        )):
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail=f"Post request for /mans/{pk} is bad")


@router.put(path="/{pk}")
async def man_update(
        session: DBSession,
        data: ManEditForm,
        pk: int = Path(
            default=...,
            ge=1,
            title="Man ID",
            examples=[42]
        ),
):
    """Обновление данных о человеке с id=pk"""
    obj = await crud.get_man_by_id(session=session, pk=pk)

    # if data.name != obj.name:
    #     ...
    # if data.surname != obj.surname:
    #     ...
    # if data.phone != obj.phone:
    #     ...
    # if data.departments != obj.departments:
    #     ...


@router.delete(path="/{pk}")
async def man_delete(
        session: DBSession,
        pk: int = Path(
            default=...,
            ge=1,
            title="Man ID",
            examples=[42]
        )
):
    """Удаление человека по id"""
    try:
        obj = await crud.delete_man_by_id(session=session, pk=pk)
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Man Doesn't exist")
    else:
        return ManDetailWithoutDepartments.model_validate(obj=obj, from_attributes=True)
