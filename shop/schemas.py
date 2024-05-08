from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class DepartmentCreateForm(BaseModel):
    dep_name: str = Field(
        default=...,
        min_length=5,
        max_length=32,
        title="Departments Name",
        examples=["Fruits", "Milk"]
    )
    id: int = Field(
        default=None,
        title="Departments ID"
    )
    # mans: list[PositiveInt] = Field(
    #     default=[34],
    #     min_length=1,
    #     title="Mans IDs who work in department.",
    #     examples=[1, 2]
    # )


class DepartmentEditForm(DepartmentCreateForm):
    ...


class DepartmentDetail(DepartmentCreateForm):
    id: PositiveInt = Field(    # Maybe delete this?
        default=...,
        title="Departments ID",
        examples=[2, 3]
    )


class ManCreateForm(BaseModel):
    name: str = Field(
        default=...,
        min_length=2,
        max_length=20,
        title="mans Name",
        examples=["Den"]
    )
    surname: str = Field(
        default=...,
        min_length=2,
        max_length=20,
        title="mans Surname",
        examples=["Pupkin"]
    )
    phone: str = Field(
        default=...,
        min_length=12,
        max_length=12,
        title="Mans Phone",
        examples=["375295955669"]
    )
    departments: list[PositiveInt] = Field(
        default=...,
        min_length=1,
        title="Departments IDs where this man can work"
    )


class ManEditForm(ManCreateForm):
    ...


class ManDetailWithoutDepartments(BaseModel):
    id: int = Field(
        default=...,
        title="Man ID",
        examples=[42]
    )
    name: str = Field(
        default=...,
        min_length=2,
        max_length=20,
        title="mans Name",
        examples=["Den", "Ivan", "Pupka"]
    )
    surname: str = Field(
        default=...,
        min_length=2,
        max_length=20,
        title="mans Surname",
        examples=["Pupkin", "Pushkin", "Kakahin"]
    )
    slug: str = Field(
        default=...,
        min_length=2,
        max_length=40,
        title="Mans slug"
    )
    phone: str = Field(
        default=...,
        min_length=12,
        max_length=12,
        title="Mans Phone",
        examples=["375291234567"]
    )
    date_add: datetime = Field(
        default=...,
        title="Date of created topic"
    )


class ManDetail(ManDetailWithoutDepartments):
    departments: list[DepartmentDetail] | None = Field(
        default=None,
        min_length=0,
        title="Departments Mans"
    )
