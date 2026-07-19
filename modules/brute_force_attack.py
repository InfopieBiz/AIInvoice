"""Brute-force attack simulator module."""

from utils.cli_helpers import clear_screen, pause, print_header


def run_brute_force_attack() -> None:
    """Display the placeholder brute-force attack screen."""
    clear_screen()
    print_header("BRUTE-FORCE ATTACK SIMULATOR")

    print(
        """
This module will eventually:

- Ask the user to enter a short test password
- Let the user select a character set
- Generate possible character combinations
- Count the number of attempts
- Measure the time taken
- Stop when the password is found
- Enforce safe attempt and time limits

Status: Not implemented yet.
"""
    )

    pause()