import json
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import src.controller.auth_controller as auth_controller
from src.schema.user_schema import UserLogin
from src.config.hash import pwd_context


def make_request_with_cookie(token_value: str) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(b"cookie", f"access_token={token_value}".encode())],
        "query_string": b"",
        "server": ("testserver", 80),
        "client": ("testclient", 12345),
    }
    return Request(scope)


def test_login_success_sets_cookie_and_returns_user(monkeypatch):
    # Prepare a fake user with hashed password and role
    hashed = pwd_context.hash("secret")
    fake_user = SimpleNamespace(
        id=1,
        name="Doe",
        firstname="John",
        email="john.doe@example.com",
        phone="01234",
        password=hashed,
        roles=[SimpleNamespace(name="user")],
    )

    # Patch get_user_by_email and create_token used inside auth_controller
    monkeypatch.setattr(auth_controller, "get_user_by_email", lambda db, email: fake_user)
    monkeypatch.setattr(auth_controller, "create_token", lambda data: SimpleNamespace(access_token="token123", token_type="Bearer"))

    resp = auth_controller.login_user(UserLogin(email="john.doe@example.com", password="secret"), db=None)

    # JSONResponse stores content in .body (bytes)
    body = json.loads(resp.body.decode())
    assert body["message"] == "Connexion réussie"
    assert body["user"]["email"] == "john.doe@example.com"
    assert body["user"]["roles"] == ["user"]

    set_cookie = resp.headers.get("set-cookie", "")
    assert "access_token=token123" in set_cookie


def test_login_wrong_password_raises_401(monkeypatch):
    hashed = pwd_context.hash("otherpass")
    fake_user = SimpleNamespace(
        id=2,
        name="Doe",
        firstname="Jane",
        email="jane.doe@example.com",
        phone="000",
        password=hashed,
        roles=[SimpleNamespace(name="user")],
    )

    monkeypatch.setattr(auth_controller, "get_user_by_email", lambda db, email: fake_user)

    with pytest.raises(HTTPException) as exc:
        auth_controller.login_user(UserLogin(email="jane.doe@example.com", password="wrong"), db=None)
    assert exc.value.status_code == 401


def test_logout_clears_cookie():
    resp = auth_controller.logout_user()
    set_cookie = resp.headers.get("set-cookie", "").lower()
    assert "access_token=" in set_cookie
    assert "max-age=0" in set_cookie or "expires=thu, 01 jan 1970" in set_cookie


def test_check_token_missing_cookie_raises():
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [],
        "query_string": b"",
        "server": ("testserver", 80),
        "client": ("testclient", 12345),
    }
    req = Request(scope)
    with pytest.raises(HTTPException) as exc:
        auth_controller.check_token(req)
    assert exc.value.status_code == 401
    assert "Token manquant" in str(exc.value.detail)


def test_check_token_valid_calls_verify(monkeypatch):
    # patch verify_token to return a payload
    monkeypatch.setattr(auth_controller, "verify_token", lambda token: {"sub": "john.doe@example.com"})
    req = make_request_with_cookie("token123")
    resp = auth_controller.check_token(req)
    assert resp["valid"] is True
    assert resp["payload"]["sub"] == "john.doe@example.com"