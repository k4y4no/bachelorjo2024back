import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status

from src.config.database import Base
from src.model.user import Role, User
from src.schema.user_schema import UserCreate
from src.controller.user_controller import create_user


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


def test_create_user_success(db_session):
    # prepare role required by create_user
    role = Role(name="user")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    payload = UserCreate(
        email="john.doe@example.com",
        password="password123",
        name="Doe",
        firstname="John",
        phone="0123456789"
    )

    resp = create_user(payload, db_session)

    # response must match UserResponse structure (dict)
    assert resp["email"] == "john.doe@example.com"
    assert resp["name"] == "Doe"
    assert resp["firstname"] == "John"
    assert isinstance(resp["roles"], list)
    assert resp["roles"] == ["user"]

    # verify user persisted in DB and password is hashed (not equal to plain)
    db_user = db_session.query(User).filter_by(email="john.doe@example.com").first()
    assert db_user is not None
    assert db_user.password != "password123"
    assert any(r.name == "user" for r in db_user.roles)


def test_create_user_duplicate_email_raises(db_session):
    # create role and a first user
    role = Role(name="user")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)

    payload = UserCreate(
        email="jane.doe@example.com",
        password="pwd",
        name="Doe",
        firstname="Jane",
        phone="000"
    )

    # first creation OK
    create_user(payload, db_session)

    # second creation with same email must raise 400
    with pytest.raises(HTTPException) as exc:
        create_user(payload, db_session)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert "already" in str(exc.value.detail) or "used" in str(exc.value.detail)