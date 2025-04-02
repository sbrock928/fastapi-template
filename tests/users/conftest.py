"""
Common fixtures for user tests.
"""

import pytest
from typing import Dict, Any


@pytest.fixture()
def user_payload(
    first_name: str = "Alice", last_name: str = "Smith", email: str = "alice@example.com"
) -> Dict[str, str]:
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }


@pytest.fixture()
def user_response(
    user_id: int = 1,
    first_name: str = "Alice",
    last_name: str = "Smith",
    email: str = "alice@example.com",
) -> Dict[str, Any]:
    return {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }
