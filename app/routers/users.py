from fastapi import APIRouter, Depends
from typing import Annotated, List
from sqlalchemy.orm import Session
from app.database import get_db
from app import database_models
from app import pydantic_models
from app import utils

router = APIRouter()

@router.get("/")
async def get_users(db: Annotated[Session, Depends(get_db)]):
    users_retrived: List[database_models.Users]=db.query(database_models.Users).all()

    return users_retrived

@router.post("/")
async def create_user(db: Annotated[Session, Depends(get_db)], user: pydantic_models.UserToCreate):
    new_user = database_models.Users()
    new_user.hashed_password = utils.hash(user.password)
    new_user.username = user.username

    db.add(new_user)
    db.commit()

    return {"resultado": "usuario creado exitosamente"}