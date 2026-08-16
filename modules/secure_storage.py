"""Secure password storage demonstration module."""

import hashlib
from getpass import getpass

from config import MAX_PASSWORD_LENGTH
from utils.cli_helpers import clear_screen, pause, print_header


def sha256_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def run_secure_storage_demo() -> None:
    """Demonstrate plaintext password storage and SHA-256 hashing."""
    clear_screen()
    print_header("SECURE STORAGE DEMONSTRATION")

    password = getpass("Enter a password to demonstrate secure storage: ")

    if not password:
        print("\nPassword cannot be empty.")
        pause()
        return

    if len(password) > MAX_PASSWORD_LENGTH:
        print(f"\nPassword cannot exceed {MAX_PASSWORD_LENGTH} characters.")
        pause()
        return

    hashed_password = sha256_hash(password)

    print(
    """
------------------------------------------------------------
PLAINTEXT STORAGE
------------------------------------------------------------

Stored value:
[Original password would be directly readable]

Risk:
If an attacker gained access to a plaintext password,
the original password would immediately be exposed.
"""
    )

    print(
    f"""
------------------------------------------------------------
SHA-256 HASHED STORAGE
------------------------------------------------------------

Original password:
[hidden]

Stored hash:
{hashed_password}

Why is this safer?

Plaintext storage means that the original password is readable directly.

Instead of the password itself, the stored value is the SHA-256 hash of the password for hashing.

In the event of a breach of the stored password data, the stored value would not be directly visible as the original password.

Hashing is a one way process . It is different to encryption .

Note:
This is for educational demonstration using SHA-256.
Dedicated password-hashing algorithms, with additional protections, are used by standard password storage systems.
"""
    )
    pause()