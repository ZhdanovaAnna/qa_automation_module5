import pytest
import requests
import uuid
import allure
from pages.login_page import LoginPage

BASE_URL = "https://demoqa.com"
HEADERS = {"Content-Type": "application/json"}


@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.navigate(lp.URL)
    return lp


@pytest.fixture(scope="function")
def fresh_user():
    """Создаёт уникального пользователя через API для теста успешного входа."""
    username = f"ui_user_{uuid.uuid4().hex[:8]}"
    password = "ValidPass1!"
    r = requests.post(
        f"{BASE_URL}/Account/v1/User",
        json={"userName": username, "password": password},
        headers=HEADERS,
    )
    if r.status_code != 201:
        pytest.skip(
            f"Не удалось создать пользователя. Статус: {r.status_code}, тело: {r.text[:200]}"
        )
    return {"username": username, "password": password}


@allure.feature("Book Store Login")
class TestLoginUI:

    @allure.story("Smoke: форма логина отображается")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.ui
    def test_smoke_elements_visible(self, login_page):
        """TC-01: Smoke — элементы формы видны."""
        with allure.step("Проверить, что поля Username, Password и кнопка Login видны"):
            assert login_page.is_form_visible()

    @allure.story("Успешная авторизация")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_successful_login(self, login_page, fresh_user):
        """TC-02: Успешный вход с валидными данными."""
        with allure.step("Заполнить Username"):
            login_page.fill_username(fresh_user["username"])
        with allure.step("Заполнить Password"):
            login_page.fill_password(fresh_user["password"])
        with allure.step("Нажать Login"):
            login_page.click_login()
        with allure.step("Проверить редирект на профиль"):
            login_page.page.wait_for_url("**/profile", timeout=10000)
            assert login_page.is_profile_opened()

    @allure.story("Неверный пароль")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_invalid_password(self, login_page):
        """TC-03: Ошибка при неверном пароле."""
        with allure.step("Заполнить Username (валидный формат)"):
            login_page.fill_username("some_invalid_user")
        with allure.step("Заполнить неверный Password"):
            login_page.fill_password("wrong_password")
        with allure.step("Нажать Login"):
            login_page.click_login()
        with allure.step("Проверить, что отображается сообщение об ошибке"):
            assert login_page.is_error_visible()

    @allure.story("Пустой Username")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_empty_username(self, login_page):
        """TC-04: Ошибка при пустом Username (форма не отправляется)."""
        with allure.step("Оставить Username пустым, заполнить Password"):
            login_page.fill_password("SomePass1!")
        with allure.step("Нажать Login"):
            login_page.click_login()
        with allure.step("Проверить, что остались на странице логина"):
            assert "login" in login_page.page.url
            assert not login_page.is_profile_opened()

    @allure.story("Пустой Password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_empty_password(self, login_page):
        """TC-05: Ошибка при пустом Password (форма не отправляется)."""
        with allure.step("Оставить Password пустым, заполнить Username"):
            login_page.fill_username("some_user")
        with allure.step("Нажать Login"):
            login_page.click_login()
        with allure.step("Проверить, что остались на странице логина"):
            assert "login" in login_page.page.url
            assert not login_page.is_profile_opened()