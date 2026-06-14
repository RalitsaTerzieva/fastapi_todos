from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from models import Todos, Users
from routers.todos import get_current_user, get_db
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost/TodoApplicationTestDatabase'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'codingwithrobytest', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_user():
    user = Users(
        id=1,
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

@pytest.fixture
def test_todo(test_user):
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
         owner_id=test_user.id,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Learn to code!"
    assert data[0]["owner_id"] == test_todo.owner_id

def test_read_one_authenticated(test_todo):
    response = client.get(f"/todo/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    
    assert data["title"] == "Learn to code!"
    assert data["owner_id"] == test_todo.owner_id

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}

def test_create_todo(test_todo):
    request_data = {
        "title": "Visit Norway",
        "description": "Make my dream come true!",
        "priority": 1,
        "complete": False    
    }

    response = client.post("/todo", json=request_data)

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == request_data["title"]
    assert data["description"] == request_data["description"]
    assert data["priority"] == request_data["priority"]
    assert data["complete"] == request_data["complete"]


def test_update_todo(test_todo):
    request_data = {
        "title": "Visit Norway",
        "description": "Make my dream come true!",
        "priority": 1,
        "complete": False    
    }

    response = client.put(f"/todo/{test_todo.id}", json=request_data)

    assert response.status_code == 204

    db = TestingSessionLocal()
    updated_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()

    assert updated_todo.title == request_data["title"]
    assert updated_todo.description == request_data["description"]
    assert updated_todo.priority == request_data["priority"]
    assert updated_todo.complete == request_data["complete"]