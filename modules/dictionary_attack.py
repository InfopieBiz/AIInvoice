"""
Dictionary attack simulator module.
"""

from __future__ import annotations

from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
from time import perf_counter
from datetime import datetime

from models.results import TestResult
from config import MAX_PASSWORD_LENGTH, WORDLIST_PATH
from utils.cli_helpers import (
    clear_screen,
    pause,
    print_error,
    print_header,
    print_success,
    print_warning,
)



class WordlistLoadError(Exception):
    """Triggered when the dictionary wordlist cannot be loaded."""


@dataclass(frozen=True)
class DictionaryAttackResult:
    """Store the result of a dictionary attack simulation."""

    success: bool
    attempts: int
    total_candidates: int
    elapsed_seconds: float


def load_wordlist(file_path: Path) -> list[str]:
    """
    Load password candidates from a text file.

    Blank lines are ignored. Each remaining line becomes one
    dictionary attack candidate.
    """
    try:
        with file_path.open(
            mode="r",
            encoding="utf-8",
        ) as wordlist_file:
            candidates = [
                line.strip()
                for line in wordlist_file
                if line.strip()
            ]

    except FileNotFoundError as error:
        raise WordlistLoadError(
            f"The wordlist file was not found: {file_path}"
        ) from error

    except PermissionError as error:
        raise WordlistLoadError(
            f"Permission was denied while reading: {file_path}"
        ) from error

    except UnicodeDecodeError as error:
        raise WordlistLoadError(
            "The wordlist could not be decoded as UTF-8 text."
        ) from error

    except OSError as error:
        raise WordlistLoadError(
            f"The wordlist could not be read: {error}"
        ) from error

    if not candidates:
        raise WordlistLoadError(
            "The wordlist file is empty or contains only blank lines."
        )

    return candidates


def dictionary_attack(
    target_password: str,
    wordlist: list[str],
) -> DictionaryAttackResult:
    """
    Attempt to find a password through exact dictionary comparison.

    The comparison is case-sensitive. The function stops immediately
    after finding a matching candidate.
    """
    attempts = 0
    start_time = perf_counter()

    for candidate in wordlist:
        attempts += 1

        if candidate == target_password:
            elapsed_seconds = perf_counter() - start_time

            return DictionaryAttackResult(
                success=True,
                attempts=attempts,
                total_candidates=len(wordlist),
                elapsed_seconds=elapsed_seconds,
            )

    elapsed_seconds = perf_counter() - start_time

    return DictionaryAttackResult(
        success=False,
        attempts=attempts,
        total_candidates=len(wordlist),
        elapsed_seconds=elapsed_seconds,
    )


def read_password_securely() -> str:
    """ Request a password without displaying it in the terminal, rejects empty and long passwords. """

    while True:
        try:
            password = getpass(
                "Enter a password for the dictionary test: "
            )

        except EOFError:
            print_error("No password input was received.")
            continue

        if not password:
            print_error("Password cannot be empty.")
            continue

        if len(password) > MAX_PASSWORD_LENGTH:
            print_error(
                f"Password cannot exceed "
                f"{MAX_PASSWORD_LENGTH} characters."
            )
            continue

        return password

    
def calculate_attempt_rate(
    attempts: int,
    elapsed_seconds: float,
) -> float:
    """
    Calculate the average number of attempts per second.

    A zero value is returned when the measured duration is zero
    or negative.
    """
    if elapsed_seconds <= 0:
        return 0.0

    return attempts / elapsed_seconds


def display_attack_result(
    result: DictionaryAttackResult,
) -> None:
    """Display the dictionary attack result without showing the password."""

    print("\n" + "-" * 64)
    print("DICTIONARY ATTACK RESULT")
    print("-" * 64)

    if result.success:
        print_success(
            "The password was found in the dictionary."
        )

        print(
            "\nThis password is vulnerable to a dictionary attack using the current wordlist."
        )

    else:
        print_warning(
            "The password was not found in the current dictionary."
        )

        print(
            "\nThis does not prove that the password is secure. "
            "Another or larger wordlist may still contain it."
        )

    attempt_rate = calculate_attempt_rate(
        result.attempts,
        result.elapsed_seconds,
    )

    print(f"\nAttempts made:       {result.attempts:,}")
    print(f"Wordlist candidates: {result.total_candidates:,}")
    print(
        f"Time taken:          "
        f"{result.elapsed_seconds:.9f} seconds"
    )

    if attempt_rate > 0:
        print(
            f"Average speed:       "
            f"{attempt_rate:,.0f} attempts/second"
        )

    if result.success:
        print(
            "\nRecommendation:\n"
            "Avoid common passwords, common words, names, dates, "
            "and predictable variations."
        )

    else:
        print(
            "\nRecommendation:\n"
            "Continue using a long, unique password and do not reuse "
            "it across multiple accounts."
        )


def run_dictionary_attack(session_results: list[TestResult],) -> None:
    """Run the interactive dictionary attack simulator."""
    clear_screen()
    print_header("DICTIONARY ATTACK SIMULATOR")

    print(
        "\nThis educational module compares a user-entered password "
        "against a local list of common passwords."
    )

    print(
        "\nComparison mode: Exact and case-sensitive"
        "\nThe entered password is hidden and is not saved.\n"
    )

    try:
        wordlist = load_wordlist(WORDLIST_PATH)

    except WordlistLoadError as error:
        print_error(str(error))

        print(
            "\nThe dictionary attack cannot run until a valid "
            "wordlist file is available."
        )

        pause()
        return

    print_success(
        f"Loaded {len(wordlist):,} password candidates."
    )

    password = read_password_securely()

    result = dictionary_attack(
        target_password=password,
        wordlist=wordlist,
    )

    session_results.append(
        TestResult(
            test_type="Dictionary Attack",
            status=result.success,
            rating=None,
            attempts=result.attempts,
            elapsed_seconds=result.elapsed_seconds,
            timestamp=datetime.now(),
        )
    )
    
    display_attack_result(result)
    
    # Remove the local reference when it is no longer needed.
    del password

    pause()