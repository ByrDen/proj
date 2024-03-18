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
    # mans: list[PositiveInt] = Field(
    #     default=[34],
    #     min_length=1,
    #     title="Mans IDs who work in department.",
    #     examples=[1, 2]
    # )


class DepartmentEditForm(DepartmentCreateForm):
    ...


class DepartmentDetail(DepartmentCreateForm):
    id: PositiveInt = Field(
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
    department_id: list[PositiveInt] = Field(
        default=...,
        min_length=0,
        title="Departments IDs where this man can work"
    )


class ManEditForm(ManCreateForm):
    ...


class ManDetail(BaseModel):
    id: PositiveInt = Field(
        default=...,
        title="Man ID",
        examples=[42]
    )
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
        examples=["375295955669"]
    )
    date_add: datetime = Field(
        default=...,
        title="Date of created topic"
    )
    departments: list[DepartmentDetail] = Field(
        default=...,
        min_length=0,
        title="Departments Mans"
    )
