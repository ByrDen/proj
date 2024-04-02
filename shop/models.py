from datetime import datetime, UTC
from typing import TYPE_CHECKING

from slugify import slugify
from sqlalchemy import Column, VARCHAR, TIMESTAMP, INT, ForeignKey, inspect
from sqlalchemy.orm import relationship

from src.models import Base


class SalesMan(Base):
    man_id = Column(
        INT,
        ForeignKey(
            column="shop_man.id",
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        # nullable=False,
        primary_key=True,
        index=True

    )
    department_id = Column(
        INT,
        ForeignKey(
            column="shop_department.id",
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        # nullable=False,
        primary_key=True,
        index=True
    )


class Man(Base):
    if TYPE_CHECKING:
        id: int
        name: str
        surname: str
        slug: str
        phone: str
        date_add: datetime
        departments: list["Department"]
    else:
        id = Column(INT, primary_key=True)

        name = Column(
            VARCHAR(length=20),
            nullable=False
        )
        surname = Column(
            VARCHAR(length=20),
            nullable=False
        )
        slug = Column(
            VARCHAR(length=40),
            nullable=False,
            unique=True
        )
        phone = Column(VARCHAR(length=12))
        date_add = Column(
            TIMESTAMP(timezone=True),
            default=lambda: datetime.now(tz=UTC),
            nullable=False
        )
        departments = relationship(
            argument="Department",
            secondary=inspect(SalesMan).local_table,
            back_populates="mans",
            uselist=True,
        )

        @staticmethod
        def auto_slug_before_insert(mapper, connection, cls) -> None:
            cls.slug = slugify(" ".join([cls.name, cls.surname]), separator="_")

        def __str__(self):
            return (f"{self.slug=}\n"
                    f"{self.name=}\n"
                    f"{self.surname=}\n"
                    f"{self.phone=}\n"
                    f"{self.departments=}\n"
                    f"{self.id=}")


class Department(Base):
    id = Column(INT, primary_key=True)

    dep_name = Column(
        VARCHAR(length=32),
        unique=True,
        nullable=False
    )
    mans = relationship(
        argument="Man",
        secondary=inspect(SalesMan).local_table,
        back_populates="departments",
        uselist=True,
    )

    def __str__(self):
        return f"{self.dep_name=}"
