from fastapi import FastAPI, Depends
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

@app.get('/')
def read_all(db: db_dependency):
    return db.query(models.Todos).all()

@app.get('/todo/{todo_id}')
def read_todo(todo_id:int, db: db_dependency):
    return db.query(models.Todos).filter(models.Todos.id == todo_id).first()