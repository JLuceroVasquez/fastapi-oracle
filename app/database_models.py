from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity, Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import func

# 1. CLASE BASE DECLARATIVA
# En SQLAlchemy 2.0, heredamos de DeclarativeBase para que esta clase
# actúe como el registro central de todas nuestras tablas.
class Base(DeclarativeBase):
    pass

# 2. DEFINICIÓN DE LA TABLA
class Todos(Base):
    # Nombre exacto que tendrá la tabla en Oracle
    __tablename__ = "todos"

    # 3. CONFIGURACIÓN DE IDENTIDAD (AUTOINCREMENTO)
    # Oracle usa objetos de identidad. Aquí definimos que el ID 
    # empezará en 1 y aumentará de 1 en 1 de forma automática.
    id_identity = Identity(start=1, increment=1)

    # 4. COLUMNA DE CLAVE PRIMARIA
    # Asignamos el objeto identity a la columna 'id'.
    # Oracle creará internamente una 'Sequence' vinculada a esta columna.
    id =Column(Integer, id_identity, primary_key=True)

    title=Column(String(50), unique=True, nullable=False)
    description=Column(String(50), nullable=False)

    owner_username=Column(String(50), ForeignKey("users.username", ondelete="CASCADE"), nullable=False)

    created_at=Column(TIMESTAMP(timezone=True), default=func.current_timestamp())

class Users(Base):
    # Nombre exacto que tendrá la tabla en Oracle
    __tablename__ = "users"

    # 3. CONFIGURACIÓN DE IDENTIDAD (AUTOINCREMENTO)
    # Oracle usa objetos de identidad. Aquí definimos que el ID 
    # empezará en 1 y aumentará de 1 en 1 de forma automática.
    id_identity = Identity(start=1, increment=1)

    # 4. COLUMNA DE CLAVE PRIMARIA
    # Asignamos el objeto identity a la columna 'id'.
    # Oracle creará internamente una 'Sequence' vinculada a esta columna.
    id =Column(Integer, id_identity, primary_key=True)

    username=Column(String(50), unique=True, nullable=False)
    hashed_password=Column(String(100), nullable=False)

    created_at=Column(TIMESTAMP(timezone=True), default=func.current_timestamp())