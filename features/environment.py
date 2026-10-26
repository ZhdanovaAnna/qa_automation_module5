from playwright.sync_api import sync_playwright
import requests, uuid

BASE_URL = "https://demoqa.com"
HEADERS = {"Content-Type": "application/json"}

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=False)

    user = f"bdd_user_{uuid.uuid4().hex[:8]}"
    pwd = "ValidPass1!"
    r = requests.post(
        f"{BASE_URL}/Account/v1/User",
        json={"userName": user, "password": pwd},
        headers=HEADERS
    )
    if r.status_code != 201:
        raise RuntimeError(f"Не удалось создать BDD-пользователя: {r.status_code}, {r.text[:200]}")
    context.valid_user = user
    context.valid_password = pwd

def before_scenario(context, scenario):
    context.context = context.browser.new_context()
    context.page = context.context.new_page()

def after_scenario(context, scenario):
    context.context.close()

def after_all(context):
    context.browser.close()
    context.playwright.stop()