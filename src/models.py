import re

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(self):
        return re.sub(
            pattern=r"(?<!^)(?=[A-Z])",
            repl="_",
            string=self.__module__.split(".")[0] + self.__name__
        ).lower()
