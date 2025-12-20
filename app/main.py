from typing import Annotated
from fastapi import FastAPI, Depends
from app import database
from sqlalchemy.orm import Session
from app import database_models

app = FastAPI()

@app.get("/")
async def get_root_with_db(db: Annotated[Session, Depends(database.get_db)]):

    all_results = db.query(database_models.TestTable).all()

    return all_results
