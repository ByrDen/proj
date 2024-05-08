from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shop.models import Man, Department
from shop.schemas import ManCreateForm


async def get_man_by_id(session: AsyncSession, pk: int) -> Man | None:
    return await session.get(
        entity=Man,
        ident=pk)


async def get_departments_by_id(
        session: AsyncSession,
        pks: list[int] | int):  # -> list[Department | None]:
    stmt = select(Department)

    if isinstance(pks, list):
        stmt = stmt.filter(Department.id.in_(pks))

    if isinstance(pks, int):
        stmt = stmt.where(Department.id == pks)
    deps = await session.scalars(statement=stmt)
    return deps.all()


async def create_man(
        session: AsyncSession,
        data: ManCreateForm,
):
    obj = Man(
        name=data.name.title(),
        surname=data.surname.title(),
        phone=data.phone,
    )
    deps = await get_departments_by_id(session=session, pks=data.departments)

    obj.departments.extend(deps)
    session.add(instance=obj)
    await session.commit()
    await session.refresh(instance=obj)
    stmt = select(Man).where(Man.id == obj.id).options(selectinload(Man.departments))
    obj_with_dep = await session.scalars(statement=stmt)
    return obj_with_dep.all()


async def update_man(
        session: AsyncSession,
        pk: int,
        data: ManCreateForm
) -> Man:
    obj = await get_man_by_id(session, pk)

    return obj                      # no tested


async def delete_man_by_id(session: AsyncSession, pk) -> Man:

    obj = await get_man_by_id(session=session, pk=pk)
    if obj:
        await session.delete(instance=obj)
        await session.commit()
    else:
        raise AttributeError
    return obj


async def update_departments_for_man(
        session: AsyncSession,
        pk: int,
        departments: list[Department]
) -> None:
    try:
        obj = get_man_by_id(session=session, pk=pk)
        if [dep.id for dep in obj.departments] == departments:
            raise IndentationError
        obj.departments = departments
    except ValueError:          # Incorrect
        raise ValueError        # Need Fix
    else:
        session.add(obj)
        await session.flush()
        # return list(obj)
