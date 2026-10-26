import pytest
from app.validators import validate_password, validate_username

class TestPasswordValidation:
    @pytest.mark.unit
    @pytest.mark.parametrize("pwd,expected", [
        ("ValidPass1!", True),
        ("Short1!", False),        # Меньше 8
        ("alllowercase1!", False), # Нет заглавной
        ("ALLUPPERCASE1!", False), # Нет строчной
        ("NoDigits!", False),      # Нет цифры
        ("", False),
    ])
    def test_validate_password(self, pwd, expected):
        assert validate_password(pwd) == expected

class TestUsernameValidation:
    @pytest.mark.unit
    @pytest.mark.parametrize("user,expected", [
        ("Ivan", True),
        ("Iv", False),
        ("", False),
    ])
    def test_validate_username(self, user, expected):
        assert validate_username(user) == expected