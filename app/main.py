from typing import Annotated
from fastapi import FastAPI, Depends
from app import database
from sqlalchemy.orm import Session
from app import database_models

# 1. INICIALIZACIÓN DE LA APLICACIÓN
# Creamos la instancia principal de FastAPI.
app = FastAPI()

# 2. DEFINICIÓN DEL ENDPOINT
# Este decorador indica que el endpoint responde a peticiones HTTP GET en la raíz (/)
@app.get("/")
async def get_root_with_db(
    # 3. INYECCIÓN DE DEPENDENCIA DE LA BASE DE DATOS
    # Annotated: Define que el parámetro 'db' es de tipo SQLAlchemy Session.
    # Depends(database.get_db): Llama a la función que configuramos en database.py.
    # Esto garantiza que:
    #   a) Se abra una conexión del pool.
    #   b) Se entregue a esta función.
    #   c) Se cierre automáticamente al terminar la petición (gracias al finally del yield).
    db: Annotated[Session, Depends(database.get_db)]
    ):

    # 4. CONSULTA A LA BASE DE DATOS
    # db.query(...): Inicia una consulta usando el modelo de SQLAlchemy.
    # .all(): Ejecuta la consulta 'SELECT * FROM test_table' y devuelve una lista de objetos.
    all_results = db.query(database_models.TestTable).all()

    # 5. RESPUESTA AL USUARIO
    # FastAPI convierte automáticamente la lista de objetos de SQLAlchemy a formato JSON.
    return all_results
