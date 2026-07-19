"""Basic password strength analyzer."""

"""
    Implemented below is basic password analyzer (stage 1) 
    - Secure hidden password input,
    - Empty-input validation, 
    - Password-length checking, and checks for lowercase letters, uppercase letters, numbers, and special characters.
    - The results are displayed in the terminal using PASS or FAIL.
"""

import string
from getpass import getpass


def read_password_securely() -> str:
    """Read a non-empty password without displaying it."""
    while True:
        try:
            password = getpass(
                "Enter a password to analyze: "
            )
        except EOFError:
            print("[ERROR] No password input was received.")
            continue

        if not password:
            print("[ERROR] Password cannot be empty.")
            continue

        return password


def check_character_classes(
    password: str,
) -> dict[str, bool]:
    """Check which character types the password contains."""
    return {
        "lowercase": any(
            character.islower()
            for character in password
        ),
        "uppercase": any(
            character.isupper()
            for character in password
        ),
        "digit": any(
            character.isdigit()
            for character in password
        ),
        "special": any(
            character in string.punctuation
            for character in password
        ),
    }


def format_check_result(check_passed: bool) -> str:
    """Return a readable PASS or FAIL result."""
    return "[PASS]" if check_passed else "[FAIL]"


def display_basic_result(
    password: str,
    checks: dict[str, bool],
) -> None:
    """Display the basic password analysis."""
    print("\n" + "-" * 50)
    print("BASIC PASSWORD ANALYSIS")
    print("-" * 50)

    print(f"\nPassword length: {len(password)}")
    print("\nCharacter checks:")

    labels = {
        "lowercase": "Contains lowercase letters",
        "uppercase": "Contains uppercase letters",
        "digit": "Contains numbers",
        "special": "Contains special characters",
    }

    for check_name, label in labels.items():
        status = format_check_result(checks[check_name])
        print(f"{status} {label}")


def run_strength_analyzer() -> None:
    """Run the basic password analyzer."""
    print("PASSWORD STRENGTH ANALYZER")
    print("The password is hidden while typing.\n")

    password = read_password_securely()
    checks = check_character_classes(password)

    display_basic_result(password, checks)


if __name__ == "__main__":
    run_strength_analyzer()