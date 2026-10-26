import re

def validate_password(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    # Минимум 1 заглавная, 1 строчная, 1 цифра
    if not re.search(r"[A-Z]", password): return False
    if not re.search(r"[a-z]", password): return False
    if not re.search(r"\d", password): return False
    return True

def validate_username(username: str) -> bool:
    return len(username) >= 3