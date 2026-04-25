from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get('/')
def read_all(db: db_dependency, status_code=status.HTTP_200_OK):
    return db.query(models.Todos).all()

@app.post('/todo', status_code=status.HTTP_200_OK)
def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
