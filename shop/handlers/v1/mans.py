from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette import status

from shop.models import Man
from shop.schemas import ManDetail, ManCreateForm, ManEditForm
from src.dependencies import DBSession

router = APIRouter(prefix="/mans",
                   tags=["Mans"])


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
    statement = select(Man).order_by(
        getattr(getattr(Man, order_by), order)()
    )
    objs = await session.execute(statement
    objs = objs.unique().scalars()
    return [ManDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.all()]


@router.post(
    path="/",
    response_model=ManDetail,
    name="shop_man_create"
)
async def man_create(
        session: DBSession,
        data: ManCreateForm
):
    """Создание человека"""
    obj = Man(
        name=data.name.upper(),
        surname=data.surname.upper(),
        phone=data.phone,
        )
    obj.slug = f"{obj.surname.lower()}-{obj.name.lower()}"
    session.add(instance=obj)
    try:
        print("Man is created!")
        await session.commit()
        await session.refresh(instance=obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Man {data.name} exist")
    else:
        return ManDetail.model_validate(obj=obj, from_attributes=True)


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


@router.get(path='/{pk}')
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
    ...


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
    ...
    """Обновление данных о человеке с id=pk"""
    ...


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
    ...
