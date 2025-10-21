from datetime import datetime, timedelta, timezone
import pytest
from fastapi import HTTPException
from starlette.requests import Request

import src.service.token_service as token_service


def make_request_with_cookie(token_value: str) -> Request:
    # strip possible "Bearer " prefix if present
    if token_value.startswith("Bearer "):
        token_value = token_value.split(" ", 1)[1]
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


def build_jwt(sub: str, secret: str, algorithm: str, expire_minutes: int) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload = {"sub": sub, "exp": exp}
    return token_service.jwt.encode(payload, secret, algorithm=algorithm)


def test_create_token_contains_access_token_and_bearer(monkeypatch):
    monkeypatch.setattr(token_service, "SECRET_KEY", "test-secret-key")
    monkeypatch.setattr(token_service, "ALGORITHM", "HS256")
    monkeypatch.setattr(token_service, "ACCESS_TOKEN_EXPIRE_MINUTES", 5)

    token = token_service.create_token({"sub": "john.doe@example.com"})
    assert token.token_type == "Bearer"
    assert isinstance(token.access_token, str) and len(token.access_token) > 0


def test_verify_token_success(monkeypatch):
    monkeypatch.setattr(token_service, "SECRET_KEY", "test-secret-key")
    monkeypatch.setattr(token_service, "ALGORITHM", "HS256")
    monkeypatch.setattr(token_service, "ACCESS_TOKEN_EXPIRE_MINUTES", 5)

    jwt_value = build_jwt("john.doe@example.com", token_service.SECRET_KEY, token_service.ALGORITHM, token_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    req = make_request_with_cookie(jwt_value)
    assert token_service.verify_token(req) is True


def test_verify_token_missing_cookie():
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
        token_service.verify_token(req)
    assert exc.value.status_code == 401
    assert "Token manquant" in str(exc.value.detail)


def test_verify_token_wrong_sub(monkeypatch):
    monkeypatch.setattr(token_service, "SECRET_KEY", "test-secret-key")
    monkeypatch.setattr(token_service, "ALGORITHM", "HS256")
    monkeypatch.setattr(token_service, "ACCESS_TOKEN_EXPIRE_MINUTES", 5)

    jwt_value = build_jwt("other.user@example.com", token_service.SECRET_KEY, token_service.ALGORITHM, token_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    req = make_request_with_cookie(jwt_value)
    with pytest.raises(HTTPException) as exc:
        token_service.verify_token(req)
    assert exc.value.status_code == 401
    assert "utilisateur non autorisé" in str(exc.value.detail)


def test_verify_token_expired(monkeypatch):
    monkeypatch.setattr(token_service, "SECRET_KEY", "test-secret-key")
    monkeypatch.setattr(token_service, "ALGORITHM", "HS256")
    # create a token already expired
    jwt_value = build_jwt("john.doe@example.com", token_service.SECRET_KEY, token_service.ALGORITHM, -10)
    req = make_request_with_cookie(jwt_value)
    with pytest.raises(HTTPException) as exc:
        token_service.verify_token(req)
    assert exc.value.status_code == 401
    assert "expiré" in str(exc.value.detail) or "invalide" in str(exc.value.detail)