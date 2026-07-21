"""
    Basic password strength analyzer.

    Stage 1: Done
    - Secure hidden password input
    - Empty-input validation
    - Password-length checking, and checks for lowercase letters, uppercase letters, numbers, and special characters
    - The results are displayed in the terminal using PASS or FAIL

    Stage 2: Done
    - Scoring based on password length
    - Character-variety points
    - Strength Rating 
    - Structured analysis results
"""

import string
from dataclasses import dataclass
from getpass import getpass


@dataclass(frozen=True)
class PasswordAnalysisResult:
    """Store the password analysis result."""

    length: int
    score: int
    rating: str
    checks: dict[str, bool]

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

def calculate_length_score(password: str) -> int:
    """Calculate points based on password length."""
    length = len(password)

    if length < 6:
        return 0
    if length < 8:
        return 10
    if length < 12:
        return 20
    if length < 16:
        return 35
    if length < 20:
        return 45

    return 50

def calculate_strength_score(
    password: str,
    checks: dict[str, bool],
) -> int:
    """Calculate the password strength score."""
    score = calculate_length_score(password)

    # Add 10 points for every character type found.
    score += sum(
        10
        for check_passed in checks.values()
        if check_passed
    )

    return max(0, min(score, 100))

def determine_strength_rating(score: int) -> str:
    """Convert the score into a strength rating."""
    if score <= 20:
        return "Very Weak"
    if score <= 40:
        return "Weak"
    if score <= 60:
        return "Moderate"
    if score <= 80:
        return "Strong"

    return "Very Strong"

def analyze_password(password: str) -> PasswordAnalysisResult:
    """Run the password checks and scoring."""
    checks = check_character_classes(password)
    score = calculate_strength_score(password, checks)
    rating = determine_strength_rating(score)

    return PasswordAnalysisResult(
        length=len(password),
        score=score,
        rating=rating,
        checks=checks,
    )

def format_check_result(check_passed: bool) -> str:
    """Return a readable PASS or FAIL result."""
    return "[PASS]" if check_passed else "[FAIL]"

def display_analysis_result(
    result: PasswordAnalysisResult,
) -> None:
    """Display the password analysis."""
    print("\n" + "-" * 50)
    print("PASSWORD ANALYSIS RESULT")
    print("-" * 50)

    print(f"\nPassword length: {result.length}")
    print(f"Strength score: {result.score}/100")
    print(f"Strength rating: {result.rating}")

    print("\nCharacter checks:")

    labels = {
        "lowercase": "Contains lowercase letters",
        "uppercase": "Contains uppercase letters",
        "digit": "Contains numbers",
        "special": "Contains special characters",
    }

    for check_name, label in labels.items():
        status = format_check_result(result.checks[check_name])
        print(f"{status} {label}")

def run_strength_analyzer() -> None:
    """Run the password strength analyzer."""
    print("PASSWORD STRENGTH ANALYZER")
    print("The password is hidden while typing.\n")

    password = read_password_securely()
    result = analyze_password(password)

    display_analysis_result(result)

if __name__ == "__main__":
    run_strength_analyzer()