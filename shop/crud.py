from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from shop.models import Man, Department
from shop.schemas import ManCreateForm


async def get_man_by_id(session: AsyncSession, pk: int) -> Man | None:
    return await session.get(
        entity=Man,
        ident=pk,
        options=[selectinload(Man.departments)])


async def create_man(
        session: AsyncSession,
        data: ManCreateForm,
) -> Man:
    obj = Man(
        name=data.name.title(),
        surname=data.surname.title(),
        phone=data.phone,
    )
    dep = await get_departments_by_id(session=session, pks=data.departments)

    event.listen(Man, "before_insert", Man.auto_slug_before_insert)

    obj.departments.extend(dep)
    session.add(instance=obj)
    try:
        await session.commit()
    except IntegrityError as e:
        raise e
    else:
        await session.refresh(instance=obj)
        return obj


async def update_man(
        session: AsyncSession,
        pk: int,
        data: ManCreateForm
) -> Man:
    obj = await get_man_by_id(session, pk)

    return obj                      # no tested


async def delete_man_by_id(session: AsyncSession, pk) -> Man:
    obj = await get_man_by_id(session=session, pk=pk)
    await session.delete(instance=obj)
    await session.commit()
    return obj          # no worked???


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
    except ValueError as e:
        print(f"{e}")
    else:
        session.add(obj)
        await session.flush()
        # return list(obj)


async def get_departments_by_id(
        session: AsyncSession,
        pks: list[int]) -> list[Department | None]:
    # try:
    #     dep = [await session.get(entity=Department, ident=pk) for pk in pks]
    # except NoResultFound:
    #     raise NoResultFound
    return [await session.get(entity=Department, ident=pk) for pk in pks]
    # stmt = select(Department).where(Department.id.in_(pks))
    # print(stmt)
    # deps = await session.scalars(statement=stmt)
    # print(list(deps.all()))
    # return list(deps.all())
    # dep = await session.get(entity=Department, ident=pk)
    # return dep
    # department = await session.scalar(
    #     select(Department).where(Department.id == pk),
    #     options=(selectinload(Department.mans),),
    # )
    # return department
