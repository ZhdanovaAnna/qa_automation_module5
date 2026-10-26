from behave import given, when, then
from pages.login_page import LoginPage

@given('пользователь находится на странице логина')
def step_navigate(context):
    context.login_page = LoginPage(context.page)
    context.login_page.navigate(LoginPage.URL)

@when('он вводит валидные данные')
def step_fill_valid(context):
    context.login_page.fill_username(context.valid_user)
    context.login_page.fill_password(context.valid_password)
    context.login_page.click_login()

@then('отображается страница профиля')
def step_check_profile(context):
    context.page.wait_for_url("**/profile", timeout=10000)
    assert context.login_page.is_profile_opened()

@when('он вводит неверный пароль')
def step_fill_invalid(context):
    context.login_page.fill_username("invalid_user")
    context.login_page.fill_password("wrong")
    context.login_page.click_login()

@then('отображается сообщение об ошибке')
def step_check_error(context):
    assert context.login_page.is_error_visible()