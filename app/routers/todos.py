from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from sqlalchemy.orm import Session
from app import database_models
from app import pydantic_models
from app import oauth2

router = APIRouter()

# 2. DEFINICIÓN DEL ENDPOINT
# Este decorador indica que el endpoint responde a peticiones HTTP GET en la raíz (/todos)
@router.get("/")
async def get_root_with_db(
    # 3. INYECCIÓN DE DEPENDENCIA DE LA BASE DE DATOS
    # Annotated: Define que el parámetro 'db' es de tipo SQLAlchemy Session.
    # Depends(database.get_db): Llama a la función que configuramos en database.py.
    # Esto garantiza que:
    #   a) Se abra una conexión del pool.
    #   b) Se entregue a esta función.
    #   c) Se cierre automáticamente al terminar la petición (gracias al finally del yield).
    db: Annotated[Session, Depends(get_db)],
    username: Annotated[str, Depends(oauth2.get_current_user)]
    ):

    list_of_todos: List[database_models.Todos]=db.query(database_models.Todos).filter(database_models.Todos.owner_username==username).all()

    # 5. RESPUESTA AL USUARIO
    # FastAPI convierte automáticamente la lista de objetos de SQLAlchemy a formato JSON.
    return list_of_todos

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: Annotated[Session, Depends(get_db)], todo: pydantic_models.Todo, username: Annotated[str, Depends(oauth2.get_current_user)]):
    
    new_todo = database_models.Todos(**todo.model_dump(), owner_username=username)

    # new_todo = database_models.Todos()
    # new_todo.title = todo.title
    # new_todo.description = todo.description

    try:
        db.add(new_todo)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="No se pudo añadir la nueva tarea")
    
    return {"resultado": "Tarea creada"}

@router.delete("/{id}")
async def delete_todo(db: Annotated[Session, Depends(get_db)], id: int, username: Annotated[str, Depends(oauth2.get_current_user)]):
    todo_with_id_query = db.query(database_models.Todos).filter(database_models.Todos.id==id, database_models.Todos.owner_username==username)
    todo_with_id = todo_with_id_query.first()

    if todo_with_id==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe la tarea con id {id}")
    
    else:
        todo_with_id_query.delete()
        db.commit()

    return {"resultado": "Tarea eliminada"}

@router.put("/{id}")
async def update_todo(db: Annotated[Session, Depends(get_db)], id: int, todo: pydantic_models.Todo, username: Annotated[str, Depends(oauth2.get_current_user)]):
    todo_with_id_query = db.query(database_models.Todos).filter(database_models.Todos.id==id, database_models.Todos.owner_username==username)
    todo_with_id = todo_with_id_query.first()

    if todo_with_id==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No existe la tarea con id {id}")
    
    else:
        todo_with_id_query.update(todo.model_dump())
        db.commit()

    return todo_with_id_query.first()