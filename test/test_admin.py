from test.conftest import override_get_current_user, override_get_db, client, TestingSessionLocal, app
from models import Todos
from routers.todos import get_current_user as todos_get_current_user, get_db as todos_get_db
from routers.admin import get_db as admin_get_db
from routers.auth import get_current_user as auth_get_current_user
from fastapi import status


app.dependency_overrides[todos_get_db] = override_get_db
app.dependency_overrides[todos_get_current_user] = override_get_current_user
app.dependency_overrides[admin_get_db] = override_get_db
app.dependency_overrides[auth_get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK


def test_admin_delete_todo(test_todo):
    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == 204

    db = TestingSessionLocal()
    try:
        model = db.query(Todos).filter(Todos.id == test_todo.id).first()
        assert model is None
    finally:
        db.close()


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/9999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}