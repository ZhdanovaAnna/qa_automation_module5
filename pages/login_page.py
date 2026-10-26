from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://demoqa.com/login"
    LOCATORS = {
        "username": "#userName",
        "password": "#password",
        "login_btn": "#login",
        "error_msg": "#name",
        "profile_header": "#userName-value",
    }

    def fill_username(self, value: str):
        self.page.fill(self.LOCATORS["username"], value)

    def fill_password(self, value: str):
        self.page.fill(self.LOCATORS["password"], value)

    def click_login(self):
        self.page.click(self.LOCATORS["login_btn"])

    def is_error_visible(self) -> bool:
        locator = self.page.locator(self.LOCATORS["error_msg"])
        try:
            locator.wait_for(state="visible", timeout=15000)
            text = locator.inner_text()
            return "Invalid" in text or "invalid" in text
        except Exception:
            return False

    def is_profile_opened(self) -> bool:
        try:
            self.page.locator(self.LOCATORS["profile_header"]).wait_for(
                state="visible", timeout=10000
            )
            return True
        except Exception:
            return False

    def is_form_visible(self) -> bool:
        return (
            self.page.is_visible(self.LOCATORS["username"])
            and self.page.is_visible(self.LOCATORS["password"])
            and self.page.is_visible(self.LOCATORS["login_btn"])
        )