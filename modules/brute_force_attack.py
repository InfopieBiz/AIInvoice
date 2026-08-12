"""Controlled automatic brute-force password simulation module."""

from __future__ import annotations

import string
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
from time import perf_counter

from config import BRUTE_FORCE_PROGRESS_INTERVAL, MAX_BRUTE_FORCE_ATTEMPTS, BRUTE_FORCE_TIMEOUT_SECONDS
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


def brute_force_attack(
    target_password: str,
    charset_name: str,
    charset: str,
    maximum_length: int,
    maximum_attempts: int,
    timeout_seconds: float,
    progress_interval: int = BRUTE_FORCE_PROGRESS_INTERVAL,
) -> BruteForceResult:
    """Run a controlled brute-force search against one character set."""

    search_space = calculate_search_space(
        len(charset),
        maximum_length,
    )

    if not password_matches_charset(
        target_password,
        charset,
    ):
        return BruteForceResult(
            charset_name=charset_name,
            success=False,
            attempts=0,
            elapsed_seconds=0.0,
            stop_reason="charset_mismatch",
            search_space=search_space,
            charset_size=len(charset),
            maximum_length=maximum_length,
        )

    attempts = 0
    start_time = perf_counter()

    try:
        for candidate in generate_combinations(
            charset,
            maximum_length,
        ):
            attempts += 1

            if candidate == target_password:
                elapsed_seconds = (
                    perf_counter() - start_time
                )

                return BruteForceResult(
                    charset_name=charset_name,
                    success=True,
                    attempts=attempts,
                    elapsed_seconds=elapsed_seconds,
                    stop_reason="found",
                    search_space=search_space,
                    charset_size=len(charset),
                    maximum_length=maximum_length,
                )

            elapsed_seconds = (
                perf_counter() - start_time
            )

            if attempts >= maximum_attempts:
                return BruteForceResult(
                    charset_name=charset_name,
                    success=False,
                    attempts=attempts,
                    elapsed_seconds=elapsed_seconds,
                    stop_reason="maximum_attempts",
                    search_space=search_space,
                    charset_size=len(charset),
                    maximum_length=maximum_length,
                )

            if elapsed_seconds >= timeout_seconds:
                return BruteForceResult(
                    charset_name=charset_name,
                    success=False,
                    attempts=attempts,
                    elapsed_seconds=elapsed_seconds,
                    stop_reason="timeout",
                    search_space=search_space,
                    charset_size=len(charset),
                    maximum_length=maximum_length,
                )

    except KeyboardInterrupt:
        elapsed_seconds = (
            perf_counter() - start_time
        )

        return BruteForceResult(
            charset_name=charset_name,
            success=False,
            attempts=attempts,
            elapsed_seconds=elapsed_seconds,
            stop_reason="cancelled",
            search_space=search_space,
            charset_size=len(charset),
            maximum_length=maximum_length,
        )

    elapsed_seconds = (
        perf_counter() - start_time
    )

    return BruteForceResult(
        charset_name=charset_name,
        success=False,
        attempts=attempts,
        elapsed_seconds=elapsed_seconds,
        stop_reason="search_exhausted",
        search_space=search_space,
        charset_size=len(charset),
        maximum_length=maximum_length,
    )


def brute_force_all_charsets(
    target_password: str,
    maximum_length: int,
) -> list[BruteForceResult]:
    """Automatically test supported character sets in order."""

    if len(target_password) > maximum_length:
        return []

    results: list[BruteForceResult] = []

    overall_start = perf_counter()
    total_attempts = 0

    for charset_name, charset in CHARACTER_SETS:
        overall_elapsed = (
            perf_counter() - overall_start
        )

        remaining_attempts = (
            MAX_BRUTE_FORCE_ATTEMPTS
            - total_attempts
        )

        remaining_time = (
            BRUTE_FORCE_TIMEOUT_SECONDS
            - overall_elapsed
        )

        if remaining_attempts <= 0:
            break

        if remaining_time <= 0:
            break

        if not password_matches_charset(
            target_password,
            charset,
        ):
            search_space = calculate_search_space(
                len(charset),
                maximum_length,
            )

            result = BruteForceResult(
                charset_name=charset_name,
                success=False,
                attempts=0,
                elapsed_seconds=0.0,
                stop_reason="charset_mismatch",
                search_space=search_space,
                charset_size=len(charset),
                maximum_length=maximum_length,
            )

            results.append(result)
            continue

        result = brute_force_attack(
            target_password=target_password,
            charset_name=charset_name,
            charset=charset,
            maximum_length=maximum_length,
            maximum_attempts=remaining_attempts,
            timeout_seconds=remaining_time,
        )

        results.append(result)
        total_attempts += result.attempts

        if result.success:
            break

        if result.stop_reason in {
            "cancelled",
            "maximum_attempts",
            "timeout",
        }:
            break

    return results


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