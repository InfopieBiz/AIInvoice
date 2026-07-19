"""Reusable command-line interface helper functions."""

import os
from collections.abc import Iterable


SEPARATOR_WIDTH = 64


def clear_screen() -> None:
    """Clear the terminal window on Windows, macOS, or Linux."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def print_header(title: str) -> None:
    """
    Print a consistently formatted screen heading.

    Args:
        title: The heading displayed to the user.
    """
    print("=" * SEPARATOR_WIDTH)
    print(title.center(SEPARATOR_WIDTH))
    print("=" * SEPARATOR_WIDTH)


def print_subheader(title: str) -> None:
    """Print a smaller section heading."""
    print(f"\n--- {title} ---")


def print_success(message: str) -> None:
    """Print a success message."""
    print(f"\n[+] {message}")


def print_warning(message: str) -> None:
    """Print a warning message."""
    print(f"\n[!] {message}")


def print_error(message: str) -> None:
    """Print an error message."""
    print(f"\n[-] {message}")


def pause(message: str = "Press Enter to return to the main menu...") -> None:
    """
    Pause execution until the user presses Enter.

    EOFError may happen when input is unavailable, such as when a program
    is run through certain automated environments.
    """
    try:
        input(f"\n{message}")
    except EOFError:
        pass


def get_menu_choice(
    valid_choices: Iterable[str],
    prompt: str = "Select an option: ",
) -> str:
    """
    Repeatedly request input until the user enters a valid menu choice.

    Args:
        valid_choices: Values accepted by the menu.
        prompt: Message displayed before reading input.

    Returns:
        A validated menu choice as a string.
    """
    allowed_choices = set(valid_choices)

    while True:
        try:
            choice = input(prompt).strip()

            if choice in allowed_choices:
                return choice

            choices_text = ", ".join(sorted(allowed_choices))
            print_error(
                f"Invalid option. Please choose one of: {choices_text}"
            )

        except EOFError:
            print_error("No input was received.")
        except KeyboardInterrupt:
            print("\n")
            raise