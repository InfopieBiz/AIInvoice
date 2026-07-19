"""Application-wide configuration values."""

APP_NAME = "Password Security Analyzer"
APP_VERSION = "1.0.0"

ETHICAL_USE_NOTICE = """
This application is intended only for cybersecurity education.

It may only be used to test passwords entered directly by the user
inside this local application.

Do not use this software to attack accounts, websites, networks,
devices, databases, or systems without explicit authorization.

The dictionary and brute-force modules are controlled demonstrations.
"""

MAIN_MENU_OPTIONS = {
    "1": "Password Strength Analyzer",
    "2": "Dictionary Attack Simulator",
    "3": "Brute Force Attack Simulator",
    "4": "Secure Storage Demonstration",
    "5": "Results Dashboard",
    "0": "Exit",
}

# Password input limits
MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 128


# Common passwords used by the strength analyzer.
# The dictionary attack module will later use a larger external file.
COMMON_PASSWORDS = frozenset(
    {
        "123456",
        "12345678",
        "123456789",
        "password",
        "password1",
        "password123",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "welcome",
        "welcome123",
        "letmein",
        "iloveyou",
        "football",
        "monkey",
        "dragon",
        "abc123",
        "user",
        "login",
    }
)


# Common words that remain predictable even when numbers or symbols
# are added around them.
COMMON_PASSWORD_WORDS = (
    "password",
    "admin",
    "welcome",
    "letmein",
    "qwerty",
    "football",
    "monkey",
    "dragon",
    "login",
    "iloveyou",
)


# Common keyboard patterns.
KEYBOARD_PATTERNS = (
    "qwerty",
    "asdf",
    "asdfgh",
    "zxcv",
    "zxcvbn",
    "qaz",
    "wsx",
    "1q2w",
    "1q2w3e",
)