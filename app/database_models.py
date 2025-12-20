from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity, Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import func


class Base(DeclarativeBase):
    pass

class Todos(Base):
    __tablename__ = "todos"

    id_identity = Identity(start=1, increment=1)
    id =Column(Integer, id_identity, primary_key=True)

    description = Column(String(50), nullable=False)