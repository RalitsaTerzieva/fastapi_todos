from test.conftest import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
  
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['username'] == 'codingwithrobytest'
    assert data['email'] == 'codingwithrobytest@email.com'
    assert data['first_name'] == 'Eric'
    assert data['last_name'] == 'Roby'
    assert data['role'] == 'admin'
    assert data['phone_number'] == '111-111-1111'

def test_change_password_success(test_user):
    request_data = {
        "password": "testpassword",
        "new_password": "newtestpassword"
    }

    response = client.put("/users/password", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT