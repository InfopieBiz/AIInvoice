"""Controlled automatic brute-force password simulation module."""

from __future__ import annotations

import string
from collections.abc import Iterator
from dataclasses import dataclass
from getpass import getpass
from itertools import product
from time import perf_counter

from config import (
    BRUTE_FORCE_PROGRESS_INTERVAL,
    BRUTE_FORCE_TIMEOUT_SECONDS,
    MAX_BRUTE_FORCE_ATTEMPTS,
    MAX_BRUTE_FORCE_LENGTH,
    MAX_PASSWORD_LENGTH,
)

from utils.cli_helpers import (
    clear_screen,
    pause,
    print_error,
    print_header,
    print_warning,
    read_integer,
)


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
        "Lowercase + uppercase letters",
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
        "All supported printable ASCII characters",
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


def read_password_securely() -> str:
    """Read and validate a hidden test password."""
    while True:
        password = getpass(
            "Enter a test password: "
        )

        if not password:
            print_error(
                "Password cannot be empty."
            )
            continue

        if len(password) > MAX_PASSWORD_LENGTH:
            print_error(
                f"Password cannot exceed "
                f"{MAX_PASSWORD_LENGTH} characters."
            )
            continue

        if not password_matches_charset(
            password,
            CHARACTER_SETS[-1][1],
        ):
            print_error(
                "Password contains unsupported characters. "
                "Please use printable ASCII characters only."
            )
            continue

        return password


def display_progress(
    charset_name: str,
    attempts: int,
    elapsed_seconds: float,
) -> None:
    """Display brute-force progress for the current charset."""

    print(
        f"\r[{charset_name}] "
        f"Attempts: {attempts:,} "
        f"| Elapsed: {elapsed_seconds:.2f}s",
        end="",
        flush=True,
    )


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

            if (
                progress_interval > 0
                and attempts % progress_interval == 0
            ):
                display_progress(
                    charset_name,
                    attempts,
                    elapsed_seconds,
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


def display_all_charset_configuration(
    maximum_length: int,
) -> None:
    """Display theoretical information for all character sets."""

    print(
        "\n"
        + "-" * 60
    )
    print(
        "AUTOMATIC CHARACTER-SET ANALYSIS"
    )
    print(
        "-" * 60
    )

    print(
        f"\nMaximum search length: "
        f"{maximum_length}"
    )

    for number, (
        charset_name,
        charset,
    ) in enumerate(
        CHARACTER_SETS,
        start=1,
    ):
        search_space = calculate_search_space(
            len(charset),
            maximum_length,
        )

        print(
            f"\n{number}. {charset_name}"
        )
        print(
            f"   Characters: {len(charset)}"
        )
        print(
            f"   Theoretical search space: "
            f"{search_space:,}"
        )

    print(
        f"\nGlobal attempt limit: "
        f"{MAX_BRUTE_FORCE_ATTEMPTS:,}"
    )
    print(
        f"Global timeout: "
        f"{BRUTE_FORCE_TIMEOUT_SECONDS:.1f} seconds"
    )


def display_all_results(
    results: list[BruteForceResult],
) -> None:
    """Display the result for every supported character set."""

    print(
        "\n"
        + "-" * 60
    )
    print(
        "CHARACTER-SET TEST RESULTS"
    )
    print(
        "-" * 60
    )

    result_lookup = {
        result.charset_name: result
        for result in results
    }

    password_found = any(
        result.success
        for result in results
    )

    for number, (
        charset_name,
        _,
    ) in enumerate(
        CHARACTER_SETS,
        start=1,
    ):
        print(
            f"\n{number}. {charset_name}"
        )

        result = result_lookup.get(
            charset_name
        )

        if result is None:
            if password_found:
                print(
                    "   Status: NOT REQUIRED"
                )
            else:
                print(
                    "   Status: NOT TESTED"
                )

            continue

        if result.success:
            status = "FOUND"

        elif (
            result.stop_reason
            == "charset_mismatch"
        ):
            status = "SKIPPED"

        elif (
            result.stop_reason
            == "maximum_attempts"
        ):
            status = (
                "STOPPED - MAXIMUM ATTEMPTS"
            )

        elif result.stop_reason == "timeout":
            status = "STOPPED - TIMEOUT"

        elif result.stop_reason == "cancelled":
            status = "CANCELLED"

        elif (
            result.stop_reason
            == "search_exhausted"
        ):
            status = "NOT FOUND"

        else:
            status = "STOPPED"

        print(
            f"   Status: {status}"
        )
        print(
            f"   Attempts: {result.attempts:,}"
        )
        print(
            f"   Search space: "
            f"{result.search_space:,}"
        )

        if (
            result.stop_reason
            != "charset_mismatch"
        ):
            print(
                f"   Time: "
                f"{result.elapsed_seconds:.6f} seconds"
            )


def display_overall_result(
    results: list[BruteForceResult],
    total_elapsed_seconds: float,
) -> None:
    """Display the overall automatic brute-force result."""

    total_attempts = sum(
        result.attempts
        for result in results
    )

    successful_result = next(
        (
            result
            for result in results
            if result.success
        ),
        None,
    )

    attempt_rate = calculate_attempt_rate(
        total_attempts,
        total_elapsed_seconds,
    )

    print(
        "\n"
        + "-" * 60
    )
    print(
        "OVERALL BRUTE-FORCE RESULT"
    )
    print(
        "-" * 60
    )

    if successful_result is not None:
        print(
            "\n[+] Test password discovered."
        )
        print(
            "\nSuccessful character set:"
        )
        print(
            successful_result.charset_name
        )

    elif (
        results
        and results[-1].stop_reason
        == "maximum_attempts"
    ):
        print(
            "\n[!] Global maximum attempt "
            "limit reached."
        )

    elif (
        results
        and results[-1].stop_reason
        == "timeout"
    ):
        print(
            "\n[!] Global brute-force "
            "timeout reached."
        )

    elif (
        results
        and results[-1].stop_reason
        == "cancelled"
    ):
        print(
            "\n[!] Brute-force simulation "
            "cancelled."
        )

    else:
        print(
            "\n[-] Test password was not "
            "discovered."
        )

    print(
        f"\nTotal live attempts: "
        f"{total_attempts:,}"
    )
    print(
        f"Total execution time: "
        f"{total_elapsed_seconds:.6f} seconds"
    )
    print(
        f"Average attempt rate: "
        f"{attempt_rate:,.0f} attempts/second"
    )
    print(
        f"Global attempt limit: "
        f"{MAX_BRUTE_FORCE_ATTEMPTS:,}"
    )
    print(
        f"Global timeout: "
        f"{BRUTE_FORCE_TIMEOUT_SECONDS:.1f} seconds"
    )

    print(
        "\nSecurity recommendation:"
    )
    print(
        "Longer passwords greatly increase "
        "the number of possible combinations."
    )


def run_brute_force_attack() -> None:
    """Run the interactive automatic brute-force simulator."""

    clear_screen()
    print_header(
        "BRUTE-FORCE ATTACK SIMULATOR"
    )

    print(
        "\nThis simulator automatically tests "
        "supported character sets in order."
    )

    print(
        "\nNo character-set selection is required."
    )

    print(
        "\nSafety limits:"
    )
    print(
        f"- Maximum brute-force length: "
        f"{MAX_BRUTE_FORCE_LENGTH}"
    )
    print(
        f"- Maximum total attempts: "
        f"{MAX_BRUTE_FORCE_ATTEMPTS:,}"
    )
    print(
        f"- Maximum total runtime: "
        f"{BRUTE_FORCE_TIMEOUT_SECONDS:.1f} seconds"
    )

    print(
        "\nPress Ctrl+C during the simulation "
        "to cancel safely."
    )

    print(
        "\nThe test password is hidden while "
        "typing and is not saved.\n"
    )

    try:
        password = read_password_securely()

        maximum_length = read_integer(
            prompt=(
                f"\nEnter maximum search length "
                f"(1-{MAX_BRUTE_FORCE_LENGTH}): "
            ),
            minimum=1,
            maximum=MAX_BRUTE_FORCE_LENGTH,
        )

        if len(password) > maximum_length:
            print_warning(
                "The password is longer than the "
                "selected maximum search length."
            )

            print(
                "\nNo brute-force attempts "
                "were performed."
            )

            del password
            pause()
            return

        display_all_charset_configuration(
            maximum_length,
        )

        print(
            "\nStarting automatic "
            "character-set tests...\n"
        )

        overall_start = perf_counter()

        results = brute_force_all_charsets(
            target_password=password,
            maximum_length=maximum_length,
        )

        total_elapsed_seconds = (
            perf_counter() - overall_start
        )

        print()

        display_all_results(
            results,
        )

        display_overall_result(
            results,
            total_elapsed_seconds,
        )

        del password

    except KeyboardInterrupt:
        print()
        print_warning(
            "Brute-force simulation cancelled."
        )

    except EOFError:
        print()
        print_warning(
            "Input was cancelled."
        )

    pause()