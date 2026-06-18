from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import models
from database import engine
from routers import admin, auth, todos, users


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/home")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")


@app.get("/")
def root():
    return RedirectResponse(url="/home")

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(todos.router)

