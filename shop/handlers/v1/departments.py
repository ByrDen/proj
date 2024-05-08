from typing import Literal

from fastapi import APIRouter, Query, Path, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from starlette import status

from shop import crud
from shop.models import Department
from shop.schemas import DepartmentDetail, DepartmentCreateForm, DepartmentEditForm
from src.dependencies import DBSession

router = APIRouter(prefix="/departments",
                   tags=["Departments"])


@router.get(
    path="/",
    response_model=list[DepartmentDetail],
    name="shop_departments_list"
)
async def departments_list(
        session: DBSession,
        order_by: Literal["id", "dep_name"] = Query(default="id", alias="orderBy"),
        order: Literal["asc", "desc"] = Query(default="asc", alias="orderDirection")
):
    """Получение всех отделов"""
    statement = select(Department).options(selectinload(Department.mans)).order_by(
        getattr(getattr(Department, order_by), order)()
    )
    objs = await session.scalars(statement=statement)
    return [DepartmentDetail.model_validate(obj=obj, from_attributes=True) for obj in objs.all()]


@router.post(
    path="/",
    response_model=DepartmentDetail,
    name="departments_create"
)
async def departments_create(
        session: DBSession,
        data: DepartmentCreateForm
):
    """Создание отдела"""
    obj = Department(dep_name=data.dep_name.upper(), id=data.id)
    session.add(instance=obj)
    try:
        await session.commit()
        await session.refresh(obj)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Department {data.dep_name.upper()} is exist!")
    else:
        return DepartmentDetail.model_validate(obj=obj, from_attributes=True)



@router.put(path="/")
async def departments_update_all():
    """Массовое Обновление всех отделов"""
    ...


@router.delete(path="/")
async def departments_delete_all():
    """Удаление всех отделов"""
    ...


@router.get(path='/{pk}')
async def department_detail(
        session: DBSession,
        pk: int = Path(
            default=...,
            ge=1,
            title="Departments ID",
            examples=[42]
        )
):
    """Детали про отдел по id={pk} """
    deps = await crud.get_departments_by_id(session=session, pks=pk)
    return DepartmentDetail.model_validate(obj=deps, from_attributes=True)


@router.post(path='/{pk}')
async def department_create(
        pk: int = Path(
            default=...,
            ge=1,
            title="department ID",
            examples=[42]
        )):
    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                        detail=f"Post request for '/departments/{pk}' is bad")


@router.put(path="/{pk}")
async def department_update(
        pk: int = Path(
            default=...,
            ge=1,
            title="Department ID",
            examples=[42]
        ),
        **kwargs
):
    """Обновление данных об отделе с id=pk из аргов или кваргов"""
    for key, values in kwargs.items():
        if not hasattr(Department, key):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete(path="/{pk}")
async def department_delete(
        pk: int = Path(
            default=...,
            ge=1,
            title="Man ID",
            examples=[42]
        )
):
    """Удаление отдела по id"""
    ...