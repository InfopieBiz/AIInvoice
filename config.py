"""Application-wide configuration values."""

APP_NAME = "Password Security Analyzer"
APP_VERSION = "1.0.0"

ETHICAL_USE_NOTICE = """
This application is intended only for cybersecurity education.

It may only be used to test passwords entered directly by the user
inside this local application.

Do not use this software to attack accounts, websites, networks,
devices, databases, or systems without explicit authorization.

The dictionary and brute-force modules are controlled demonstrations.
"""

MAIN_MENU_OPTIONS = {
    "1": "Password Strength Analyzer",
    "2": "Dictionary Attack Simulator",
    "3": "Brute Force Attack Simulator",
    "4": "Secure Storage Demonstration",
    "5": "Results Dashboard",
    "0": "Exit",
}