from datetime import datetime, UTC

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
        primary_key=True,
        index=True
    )


class Man(Base):
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
    phone = Column(VARCHAR(length=12),)
    date_add = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(tz=UTC),
        nullable=False
    )
    departments = relationship(
        argument="Department",
        secondary=inspect(SalesMan).local_table,
        back_populates="mans"
    )

    def __str__(self):
        return f"{self.surname} has id={self.id}"


class Department(Base):
    dep_name = Column(
        VARCHAR(length=32),
        unique=True,
        nullable=False
    )
    mans = relationship(
        argument="Man",
        secondary=inspect(SalesMan).local_table,
        back_populates="departments"
    )

