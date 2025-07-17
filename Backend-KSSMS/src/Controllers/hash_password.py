import bcrypt  # Import the bcrypt library for password hashing


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        str: The bcrypt-hashed password as a UTF-8 string.
    """
    # Generate a salt. bcrypt.gensalt() handles the complexity and randomness needed for the salt.
    salt = bcrypt.gensalt()

    # Hash the password using the generated salt.
    # The password must be encoded to bytes before hashing.
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    # Return the hashed password, decoded back into a UTF-8 string,
    # suitable for storage in a database.
    return hashed_password.decode("utf-8")
