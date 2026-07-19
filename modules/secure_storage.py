"""Secure password storage demonstration module."""

from utils.cli_helpers import clear_screen, pause, print_header


def run_secure_storage_demo() -> None:
    """Display the placeholder secure storage screen."""
    clear_screen()
    print_header("SECURE STORAGE DEMONSTRATION")

    print(
        """
This module will eventually:

- Compare plaintext storage with password hashing
- Generate a SHA-256 hash
- Explain why plaintext password storage is unsafe
- Demonstrate the purpose of a unique salt
- Demonstrate stronger password hashing with PBKDF2
- Verify a password without storing the original value

Status: Not implemented yet.
"""
    )

    pause()