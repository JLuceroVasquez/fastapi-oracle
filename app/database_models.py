from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity, Column, Integer, String

# 1. CLASE BASE DECLARATIVA
# En SQLAlchemy 2.0, heredamos de DeclarativeBase para que esta clase
# actúe como el registro central de todas nuestras tablas.
class Base(DeclarativeBase):
    pass

# 2. DEFINICIÓN DE LA TABLA
class TestTable(Base):
    # Nombre exacto que tendrá la tabla en Oracle
    __tablename__ = "test_table"

    # 3. CONFIGURACIÓN DE IDENTIDAD (AUTOINCREMENTO)
    # Oracle usa objetos de identidad. Aquí definimos que el ID 
    # empezará en 1 y aumentará de 1 en 1 de forma automática.
    id_identity = Identity(start=1, increment=1)

    # 4. COLUMNA DE CLAVE PRIMARIA
    # Asignamos el objeto identity a la columna 'id'.
    # Oracle creará internamente una 'Sequence' vinculada a esta columna.
    id =Column(Integer, id_identity, primary_key=True)

    # 5. COLUMNAS DE DATOS
    # String(50) se traduce como VARCHAR2(50) en Oracle.
    # unique=True: Crea un índice único (no puede haber valores repetidos).
    # nullable=False: Es obligatorio que esta columna tenga un valor (NOT NULL).
    test_column1 = Column(String(50), unique=True, nullable=False)