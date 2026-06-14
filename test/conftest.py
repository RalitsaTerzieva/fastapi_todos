from sqlalchemy.orm import sessionmaker
from database import Base
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from main import app
import pytest
from models import Users, Todos
from routers.auth import bcrypt_context
from sqlalchemy import text


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


client = TestClient(app)

@pytest.fixture(autouse=True, scope="session")
def clean_db_on_start():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
    yield

@pytest.fixture
def test_user():
    db = TestingSessionLocal()

    user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="111-111-1111"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    try:
        db.close()
        with engine.begin() as connection:
            connection.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
    except Exception:
        pass

@pytest.fixture
def test_todo(test_user):
    db = TestingSessionLocal()

    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=test_user.id
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    yield todo

    try:
        db.close()
        with engine.begin() as connection:
            connection.execute(text("TRUNCATE todos RESTART IDENTITY CASCADE;"))
    except Exception:
        pass
