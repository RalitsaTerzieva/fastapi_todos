from fastapi import APIRouter, Depends, HTTPException, Path, status, Request
from pydantic import BaseModel, Field
from core import templates
import models
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user
from starlette.responses import RedirectResponse
from core.templates import templates
from services.todo_classifier import classify_todo
from services.nlp_analysis import analyze_text


router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request)

        todos = db.query(models.Todos).filter(
            models.Todos.owner_id == user.get("id")
        ).all()

        nlp_results = {}

        for todo in todos:
            text = f"{todo.title} {todo.description or ''}"
            nlp_results[todo.id] = analyze_text(text)

        return templates.TemplateResponse(
            request=request,
            name="todo.html",
            context={
                "todos": todos,
                "user": user,
                "nlp_results": nlp_results
            }
        )

    except Exception as e:
        print("ERROR:", e)
        raise
    

@router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request)

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            request=request,
            name="add-todo.html",
            context={
                "user": user
            }
        )

    except:
        return redirect_to_login()
    

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))

        if user is None:
            return redirect_to_login()

        todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

        return templates.TemplateResponse(
            request=request,
            name="edit-todo.html",
            context={
                "todo": todo,
                "user": user
            }
        )

    except:
        return redirect_to_login()
    

@router.get('/', status_code=status.HTTP_200_OK)
def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')

@router.post('/todo', status_code=status.HTTP_200_OK)
def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized!"
        )

    # NLP analysis
    classification = classify_todo(
        todo_request.title,
        todo_request.description
    )

    # Create Todo
    todo_model = models.Todos(
        title=todo_request.title,
        description=todo_request.description,
        priority=todo_request.priority,
        complete=todo_request.complete,
        owner_id=user.get("id"),
        category=classification["category"],
        keywords=",".join(classification["keywords"])
    )

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
):

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication Failed"
        )

    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id
    ).filter(
        models.Todos.owner_id == user.get("id")
    ).first()

    if todo_model is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found."
        )

    # NLP analysis
    classification = classify_todo(
        todo_request.title,
        todo_request.description
    )

    # Update Todo
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    # Update NLP data
    todo_model.category = classification["category"]
    todo_model.keywords = ",".join(classification["keywords"])

    db.commit()
    db.refresh(todo_model)

    return todo_model

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
        .filter(models.Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get('id')).delete()


    db.commit()