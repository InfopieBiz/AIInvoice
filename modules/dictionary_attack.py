"""Dictionary attack simulator module."""

from utils.cli_helpers import clear_screen, pause, print_header


def run_dictionary_attack() -> None:
    """Display the placeholder dictionary attack screen."""
    clear_screen()
    print_header("DICTIONARY ATTACK SIMULATOR")

    print(
        """
This module will eventually:

- Ask the user to enter a test password
- Load common passwords from a local wordlist
- Compare each dictionary entry with the test password
- Count the number of attempts
- Measure the time taken
- Display whether the password was found

Status: Not implemented yet.
"""
    )

    pause()