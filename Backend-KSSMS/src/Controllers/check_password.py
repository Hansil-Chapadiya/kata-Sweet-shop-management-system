import bcrypt  # Import the bcrypt library for password hashing and verification


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a bcrypt-hashed password.

    Args:
        password (str): The plaintext password provided by the user (e.g., during login).
        hashed_password (str): The bcrypt-hashed password retrieved from the database.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.
    """
    # Encode both the plaintext and hashed passwords to bytes before comparison,
    # as bcrypt functions operate on bytes.
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
