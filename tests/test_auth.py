import pytest
from fastapi import status
from sqlalchemy.orm import Session

from app.models.user import User
from app.core import security


class TestAuthEndpoint:
    def test_login_success(self, client, test_user: User):
        form_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth", data=form_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0

    def test_login_invalid_username(self, client):
        form_data = {
            "username": "invaliduser",
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth", data=form_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client, test_user: User):
        form_data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth", data=form_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_missing_credentials(self, client):
        response = client.post("/api/v1/auth", data={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_token_validity(self, client, test_user: User):
        form_data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth", data=form_data)
        token = response.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/api/v1/products?name=test", headers=headers)

        assert protected_response.status_code != status.HTTP_401_UNAUTHORIZED

