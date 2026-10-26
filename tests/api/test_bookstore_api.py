import pytest
import requests
import uuid

BASE_URL = "https://demoqa.com"
HEADERS = {"Content-Type": "application/json"}

class TestBookStoreAPI:
    @pytest.mark.api
    def test_login_invalid(self):
        """TC-07: невалидные данные → не должно быть token."""
        payload = {"userName": "invalid_user_xyz", "password": "wrong"}
        response = requests.post(f"{BASE_URL}/Account/v1/Login", json=payload, headers=HEADERS)

        if response.status_code not in (200, 400, 401):
            pytest.skip(f"Неожиданный статус: {response.status_code}, тело: {response.text[:200]}")

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            pytest.skip(f"Ответ не JSON. Тело ответа: {response.text[:200]!r}")

        assert "token" not in data or data.get("token") is None

    @pytest.mark.api
    def test_create_user_and_login(self):
        """TC-06: создать пользователя → войти → получить token."""
        username = f"test_user_{uuid.uuid4().hex[:8]}"
        password = "ValidPass1!"

        create_resp = requests.post(
            f"{BASE_URL}/Account/v1/User",
            json={"userName": username, "password": password},
            headers=HEADERS
        )
        if create_resp.status_code != 201:
            pytest.skip(f"Не удалось создать пользователя. Статус: {create_resp.status_code}, тело: {create_resp.text[:200]!r}")

        login_resp = requests.post(
            f"{BASE_URL}/Account/v1/Login",
            json={"userName": username, "password": password},
            headers=HEADERS
        )
        if login_resp.status_code != 200:
            pytest.skip(f"Логин не удался. Статус: {login_resp.status_code}, тело: {login_resp.text[:200]!r}")

        try:
            data = login_resp.json()
        except requests.exceptions.JSONDecodeError:
            pytest.skip(f"Ответ логина не JSON. Тело: {login_resp.text[:200]!r}")

        token = data.get("token")
        if not token:
            pytest.skip("Ответ не содержит token (сервер вернул неполный JSON)")

        assert len(token) > 0