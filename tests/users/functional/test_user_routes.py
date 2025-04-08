"""
Integration tests for the user endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from typing import Dict, Any


def test_create_user(client: TestClient, user_payload: Dict[str, Any]) -> None:
    response = client.post("/users", json=user_payload)
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Alice"
    assert data["last_name"] == "Smith"
    assert data["email"] == "alice@example.com"
    assert "id" in data


def test_get_all_users(client: TestClient, user_payload: Dict[str, Any]) -> None:
    client.post("/users", json=user_payload)
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1


def test_get_user_by_id(client: TestClient, user_payload: Dict[str, Any]) -> None:
    user = client.post("/users", json=user_payload).json()
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["first_name"] == "Alice"


def test_patch_user(client: TestClient, user_payload: Dict[str, Any]) -> None:
    user = client.post("/users", json=user_payload).json()
    response = client.patch(f"/users/{user['id']}", json={"last_name": "Johnson"})
    assert response.status_code == 200
    assert response.json()["last_name"] == "Johnson"


def test_delete_user(client: TestClient, user_payload: Dict[str, Any]) -> None:
    user = client.post("/users", json=user_payload).json()
    response = client.delete(f"/users/{user['id']}")
    assert response.status_code == 200
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 404
