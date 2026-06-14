from models import Todos
from routers.todos import get_current_user, get_db
from fastapi import status
from test.conftest import *
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


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
    try:
        updated_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()

        assert updated_todo.title == request_data["title"]
        assert updated_todo.description == request_data["description"]
        assert updated_todo.priority == request_data["priority"]
        assert updated_todo.complete == request_data["complete"]
    finally:
        db.close()


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Visit Norway",
        "description": "Make my dream come true!",
        "priority": 1,
        "complete": False    
    }

    response = client.put("/todo/999", json=request_data)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_delete_todo(test_todo):
    response = client.delete(f"/todo/{test_todo.id}")

    assert response.status_code == 204

    db = TestingSessionLocal()
    try:
        deleted_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()

        assert deleted_todo is None
    finally:
        db.close()

def test_delete_todo_not_found():
    response = client.delete("/todo/999")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}