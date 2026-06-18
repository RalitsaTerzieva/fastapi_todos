from test.conftest import *
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from fastapi import status
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user_success(test_user):
    db = TestingSessionLocal()
    try:
        authenticated_user = authenticate_user(
            test_user.username,
            "testpassword",
            db
        )

        assert authenticated_user is not False
        assert authenticated_user.username == test_user.username
    finally:
        db.close()