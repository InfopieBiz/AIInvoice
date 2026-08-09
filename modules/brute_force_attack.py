"""Controlled automatic brute-force password simulation module."""

from __future__ import annotations

import string
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product

from utils.cli_helpers import clear_screen, pause, print_header


CHARACTER_SETS = (
    (
        "Lowercase letters",
        string.ascii_lowercase,
    ),
    (
        "Uppercase letters",
        string.ascii_uppercase,
    ),
    (
        "Digits",
        string.digits,
    ),
    (
        "Lowercase letters + digits",
        string.ascii_lowercase + string.digits,
    ),
    (
        "Lowercase + Uppercase letters",
        string.ascii_letters,
    ),
    (
        "Letters + digits",
        string.ascii_letters + string.digits,
    ),
    (
        "Letters + digits + symbols",
        string.ascii_letters
        + string.digits
        + string.punctuation,
    ),
    (
        "All supported printable characters",
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " ",
    ),
)


@dataclass(frozen=True)
class BruteForceResult:
    """Result for one character-set test."""

    charset_name: str
    success: bool
    attempts: int
    elapsed_seconds: float
    stop_reason: str
    search_space: int
    charset_size: int
    maximum_length: int


def calculate_search_space(
    charset_size: int,
    maximum_length: int,
) -> int:
    """Calculate combinations for lengths 1 through maximum_length."""
    return sum(
        charset_size ** length
        for length in range(1, maximum_length + 1)
    )


def generate_combinations(
    charset: str,
    maximum_length: int,
) -> Iterator[str]:
    """Generate candidates from length 1 through maximum length."""
    for length in range(1, maximum_length + 1):
        for combination in product(
            charset,
            repeat=length,
        ):
            yield "".join(combination)


def password_matches_charset(
    password: str,
    charset: str,
) -> bool:
    """Check whether every password character exists in a charset."""
    return all(
        character in charset
        for character in password
    )


def calculate_attempt_rate(
    attempts: int,
    elapsed_seconds: float,
) -> float:
    """Calculate average attempts per second."""
    if elapsed_seconds <= 0:
        return 0.0

    return attempts / elapsed_seconds


def run_brute_force_attack() -> None:
    """Display the placeholder brute-force attack screen."""
    clear_screen()
    print_header("BRUTE-FORCE ATTACK SIMULATOR")

    print(
        """
This module will eventually:

- Ask the user to enter a short test password
- Ask for a maximum search length
- Automatically evaluate all supported character sets
- Skip incompatible character sets
- Generate possible character combinations
- Count the number of attempts
- Measure the time taken
- Stop when the password is found
- Enforce global attempt and time limits

Status: Not implemented yet.
"""
    )

    pause()