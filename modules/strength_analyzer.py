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

    Stage 3: Done
    - Exact common-password detection
    - Common-word detection
    - Character-substitution normalization
    - Score penalties for predictable passwords

    Stage 4: Done
    - Detect Characters in sequence
    - Detect Keyboard Patterns
    - Detect Repeated Character 
    - Detect Repeated Blocks 
    - Detect Predictable Endings
    - Score Penalties for detected patterns

    Stage 5: Done 
    - Password-length Recommendation 
    - Suggestions for missing character types 
    - Warnings for common predictable patterns 
    - Password Uniqueness Advices 

"""

import re
import string
from dataclasses import dataclass
from getpass import getpass

from config import (
    COMMON_PASSWORDS,
    COMMON_PASSWORD_WORDS,
    KEYBOARD_PATTERNS,
    MAX_PASSWORD_LENGTH,
)


@dataclass(frozen=True)
class PasswordAnalysisResult:
    """Store the password analysis result."""
    length: int
    score: int
    rating: str
    checks: dict[str, bool]
    patterns: dict[str, bool]
    recommendations: list[str]


def read_password_securely() -> str:
    """Read a valid password without displaying it."""
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

        if len(password) > MAX_PASSWORD_LENGTH:
            print(
                f"[ERROR] Password cannot exceed "
                f"{MAX_PASSWORD_LENGTH} characters."
            )
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


def normalize_for_pattern_matching(password: str) -> str:
    """Normalize common character substitutions."""
    substitutions = str.maketrans(
        {
            "@": "a",
            "0": "o",
            "1": "i",
            "3": "e",
            "4": "a",
            "5": "s",
            "7": "t",
            "$": "s",
        }
    )
    return password.lower().translate(substitutions)


def contains_sequential_characters(
    password: str,
    minimum_sequence_length: int = 3,
) -> bool:
    """Detect ascending or descending letter and number sequences."""
    lowered_password = password.lower()

    if len(lowered_password) < minimum_sequence_length:
        return False

    for start_index in range(
        len(lowered_password) - minimum_sequence_length + 1
    ):
        section = lowered_password[
            start_index:start_index + minimum_sequence_length
        ]

        if not (section.isalpha() or section.isdigit()):
            continue

        differences = [
            ord(section[index + 1]) - ord(section[index])
            for index in range(len(section) - 1)
        ]

        ascending = all(
            difference == 1
            for difference in differences
        )

        descending = all(
            difference == -1
            for difference in differences
        )

        if ascending or descending:
            return True

    return False


def contains_keyboard_pattern(password: str) -> bool:
    """Detect common keyboard patterns and reversed patterns."""
    lowered_password = password.lower()

    return any(
        pattern in lowered_password
        or pattern[::-1] in lowered_password
        for pattern in KEYBOARD_PATTERNS
    )


def contains_repeated_characters(password: str) -> bool:
    """Detect one character repeated at least three times."""
    return (
        re.search(
            r"(.)\1{2,}",
            password,
            re.IGNORECASE,
        )
        is not None
    )


def contains_repeated_block(password: str) -> bool:
    """Detect a small block repeated multiple times."""
    return (
        re.search(
            r"(.{2,6})\1+",
            password,
            re.IGNORECASE,
        )
        is not None
    )


def has_predictable_suffix(password: str) -> bool:
    """Detect predictable password endings."""
    predictable_suffix_pattern = (
        r"(?:"
        r"123|"
        r"1234|"
        r"12345|"
        r"19\d{2}|"
        r"20\d{2}"
        r")"
        r"[!@#$%^&*?.\-_+=,~():;]*$"
    )

    return (
        re.search(
            predictable_suffix_pattern,
            password,
            re.IGNORECASE,
        )
        is not None
    )


def check_common_patterns(password: str) -> dict[str, bool]:
    """Check the password for common and predictable patterns."""
    lowercase_password = password.lower()
    normalized_password = normalize_for_pattern_matching(password)

    exact_common_password = (
        lowercase_password in COMMON_PASSWORDS
    )

    common_word = (
        not exact_common_password
        and any(
            word in normalized_password
            for word in COMMON_PASSWORD_WORDS
        )
    )

    repeated_characters = contains_repeated_characters(password)

    repeated_block = (
        not repeated_characters
        and contains_repeated_block(password)
    )

    return {
        "common_password": exact_common_password,
        "common_word": common_word,
        "sequence": contains_sequential_characters(password),
        "keyboard_pattern": contains_keyboard_pattern(password),
        "repeated_characters": repeated_characters,
        "repeated_block": repeated_block,
        "predictable_suffix": has_predictable_suffix(password),
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
    pattern_checks: dict[str, bool],
) -> int:
    """Calculate the password strength score."""
    score = calculate_length_score(password)

    score += sum(
        10
        for check_passed in checks.values()
        if check_passed
    )

    has_common_pattern = (
        pattern_checks["common_password"]
        or pattern_checks["common_word"]
    )

    has_other_pattern = any(
        pattern_checks[pattern_name]
        for pattern_name in (
            "sequence",
            "keyboard_pattern",
            "repeated_characters",
            "repeated_block",
            "predictable_suffix",
        )
    )

    # Give up to 10 points when no patterns are found.
    if not has_common_pattern:
        score += 5

    if not has_other_pattern:
        score += 5

    # Apply penalties for detected patterns.
    if pattern_checks["common_password"]:
        score -= 35
    elif pattern_checks["common_word"]:
        score -= 20

    if pattern_checks["sequence"]:
        score -= 10

    if pattern_checks["keyboard_pattern"]:
        score -= 10

    if (
        pattern_checks["repeated_characters"]
        or pattern_checks["repeated_block"]
    ):
        score -= 10

    if pattern_checks["predictable_suffix"]:
        score -= 5

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


def generate_recommendations(
    password: str,
    character_checks: dict[str, bool],
    pattern_checks: dict[str, bool],
    score: int,
) -> list[str]:
    """Create recommendations based on detected weaknesses."""
    recommendations: list[str] = []

    password_length = len(password)

    if password_length < 12:
        recommendations.append(
            "Increase the password length to at least 12 characters."
        )
    elif password_length < 16:
        recommendations.append(
            "Consider using 16 or more characters for stronger protection."
        )

    if not character_checks["lowercase"]:
        recommendations.append(
            "Add at least one lowercase letter."
        )

    if not character_checks["uppercase"]:
        recommendations.append(
            "Add at least one uppercase letter."
        )

    if not character_checks["digit"]:
        recommendations.append(
            "Add at least one number."
        )

    if not character_checks["special"]:
        recommendations.append(
            "Add at least one special character such as !, @, #, or $."
        )

    if pattern_checks["common_password"]:
        recommendations.append(
            "Do not use a commonly known password."
        )

    if pattern_checks["common_word"]:
        recommendations.append(
            "Avoid common password words, even when letters are replaced "
            "with numbers or symbols."
        )

    if pattern_checks["sequence"]:
        recommendations.append(
            "Avoid sequential characters such as abc, 123, or 321."
        )

    if pattern_checks["keyboard_pattern"]:
        recommendations.append(
            "Avoid keyboard patterns such as qwerty, asdf, or 1q2w."
        )

    if pattern_checks["repeated_characters"]:
        recommendations.append(
            "Avoid repeating the same character several times."
        )

    if pattern_checks["repeated_block"]:
        recommendations.append(
            "Avoid repeating the same word or character block."
        )

    if pattern_checks["predictable_suffix"]:
        recommendations.append(
            "Avoid predictable endings such as 123, 1234, or a year."
        )

    if score >= 61:
        recommendations.append(
            "Keep this password unique and do not reuse it on other accounts."
        )

    if score >= 81:
        recommendations.append(
            "Store it in a trusted password manager rather than memorizing "
            "many similar passwords."
        )

    return recommendations


def analyze_password(password: str) -> PasswordAnalysisResult:
    """Run the password checks and scoring."""
    checks = check_character_classes(password)
    patterns = check_common_patterns(password)

    score = calculate_strength_score(
        password,
        checks,
        patterns,
    )

    rating = determine_strength_rating(score)

    recommendations = generate_recommendations(
        password,
        checks,
        patterns,
        score,
    )

    return PasswordAnalysisResult(
        length=len(password),
        score=score,
        rating=rating,
        checks=checks,
        patterns=patterns,
        recommendations=recommendations,
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

    print("\nPattern checks:")

    pattern_labels = {
        "common_password": "Exact common password",
        "common_word": "Common password word",
        "sequence": "Sequential characters",
        "keyboard_pattern": "Keyboard pattern",
        "repeated_characters": "Repeated characters",
        "repeated_block": "Repeated word or block",
        "predictable_suffix": "Predictable ending",
    }

    detected_patterns = [
        label
        for pattern_name, label in pattern_labels.items()
        if result.patterns[pattern_name]
    ]

    if detected_patterns:
        for pattern in detected_patterns:
            print(f"[DETECTED] {pattern}")
    else:
        print("[PASS] No predictable patterns detected")

    print("\nRecommendations:")

    for number, recommendation in enumerate(
        result.recommendations,
        start=1,
    ):
        print(f"{number}. {recommendation}")

    print("\nImportant:")
    print(
         "This score is an educational estimate based on password "
         "structure. It does not guarantee that a password is secure."
    )


def run_strength_analyzer() -> None:
    """Run the password strength analyzer."""
    print("PASSWORD STRENGTH ANALYZER")
    print("The password is hidden while typing.\n")

    password = read_password_securely()
    # Remove the below line after testing PASSWORDS
    print(f"[TEST] Password entered: {password}")  
    result = analyze_password(password)

    display_analysis_result(result)


if __name__ == "__main__":
    run_strength_analyzer()