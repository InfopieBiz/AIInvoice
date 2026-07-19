"""Main entry point for the Password Security Analyzer."""

from config import (
    APP_NAME,
    APP_VERSION,
    ETHICAL_USE_NOTICE,
    MAIN_MENU_OPTIONS,
)
from modules.brute_force_attack import run_brute_force_attack
from modules.dashboard import run_dashboard
from modules.dictionary_attack import run_dictionary_attack
from modules.secure_storage import run_secure_storage_demo
from modules.strength_analyzer import run_strength_analyzer
from utils.cli_helpers import (
    clear_screen,
    get_menu_choice,
    pause,
    print_header,
    print_warning,
)


def display_ethical_use_notice() -> None:
    """Display the application's ethical-use notice."""
    clear_screen()
    print_header("ETHICAL-USE NOTICE")
    print(ETHICAL_USE_NOTICE.strip())

    print_warning(
        "By continuing, you confirm that this application will only "
        "be used for authorized educational testing."
    )

    pause("Press Enter to acknowledge and continue...")


def display_home_menu() -> None:
    """Display the main navigation menu."""
    clear_screen()
    print_header(APP_NAME.upper())

    print(f"Version: {APP_VERSION}\n")

    print(
        "A Python CLI application for studying password strength,\n"
        "password attacks, and secure password storage.\n"
    )

    for option_number, option_name in MAIN_MENU_OPTIONS.items():
        print(f"[{option_number}] {option_name}")

    print()


def display_exit_message() -> None:
    """Display a final message before closing the application."""
    clear_screen()
    print_header("APPLICATION CLOSED")

    print(
        "\nThank you for using the Password Security Analyzer.\n"
        "Remember to use long, unique passwords and enable MFA.\n"
    )


def main() -> None:
    """Run the application's main menu loop."""
    display_ethical_use_notice()

    while True:
        display_home_menu()

        choice = get_menu_choice(MAIN_MENU_OPTIONS.keys())

        if choice == "1":
            run_strength_analyzer()

        elif choice == "2":
            run_dictionary_attack()

        elif choice == "3":
            run_brute_force_attack()

        elif choice == "4":
            run_secure_storage_demo()

        elif choice == "5":
            run_dashboard()

        elif choice == "0":
            display_exit_message()
            break


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n")
        print_warning("The application was interrupted by the user.")
        print("Exiting safely.\n")