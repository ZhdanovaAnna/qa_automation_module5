import csv
import os
import time
import pytest
import requests
import uuid
from pages.login_page import LoginPage

BASE_URL = "https://demoqa.com"
HEADERS = {"Content-Type": "application/json"}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_PATH = os.path.join(BASE_DIR, "data", "test_data.csv")


def load_test_data():
    with open(CSV_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="function")
def ddt_user():
    """Создаёт пользователя через API с 3 попытками (API нестабилен)."""
    username = f"ddt_{uuid.uuid4().hex[:6]}"
    password = "ValidPass1!"

    r = None
    for attempt in range(3):
        r = requests.post(
            f"{BASE_URL}/Account/v1/User",
            json={"userName": username, "password": password},
            headers=HEADERS,
            timeout=10,
        )
        if r.status_code == 201:
            return {"username": username, "password": password}
        time.sleep(2)  # пауза перед повтором

    pytest.skip(
        f"Не удалось создать DDT-пользователя после 3 попыток: "
        f"{r.status_code}, {r.text[:200]}"
    )


@pytest.mark.ddt
@pytest.mark.parametrize("row", load_test_data())
def test_login_ddt(page, row, ddt_user):
    lp = LoginPage(page)
    lp.navigate(lp.URL)

    # Подставляем реальные данные созданного пользователя для valid_user
    username = ddt_user["username"] if row["username"] == "valid_user" else row["username"]
    password = ddt_user["password"] if row["password"] == "ValidPass1!" else row["password"]

    lp.fill_username(username)
    lp.fill_password(password)
    lp.click_login()

    if row["expected"] == "True":
        page.wait_for_url("**/profile", timeout=10000)
        assert lp.is_profile_opened()
    else:
        # Если одно из полей пустое — форма не отправляется, остаёмся на /login
        if row["username"] == "" or row["password"] == "":
            assert "login" in page.url
            assert not lp.is_profile_opened()
        else:
            # Неверный пароль при заполненном username → DemoQA показывает ошибку
            assert lp.is_error_visible()