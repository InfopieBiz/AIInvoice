"""Session results dashboard module."""

from models.results import TestResult
from utils.cli_helpers import clear_screen, pause, print_header


def display_result(
    result: TestResult,
    number: int,
) -> None:
    """Display one recorded session result."""
    print(f"\n{number}. {result.test_type}")

    print(
        f"   Status: {result.status}"
    )

    if result.rating is not None:
        print(
            f"   Rating: {result.rating}"
        )

    if result.attempts is not None:
        print(
            f"   Attempts: {result.attempts:,}"
        )

    print(
        f"   Time: "
        f"{result.elapsed_seconds:.6f} seconds"
    )

    formatted_timestamp = (
        result.timestamp.strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    )

    print(
        f"   Date: {formatted_timestamp}"
    )


def run_dashboard(session_results: list[TestResult],) -> None:
    """Display the placeholder session dashboard."""
    clear_screen()
    print_header("SESSION RESULTS DASHBOARD")

    if not session_results:
        print(
            "\nNo tests have been completed "
            "during this session."
        )

        print(
            "\nRun one of the password security "
            "demonstrations first."
        )

        pause()
        return
    
    print(
        f"\nTests completed: "
        f"{len(session_results)}"
    )

    for number, result in enumerate(
        session_results,
        start=1,
    ):
        display_result(
            result,
            number,
        )

    pause()