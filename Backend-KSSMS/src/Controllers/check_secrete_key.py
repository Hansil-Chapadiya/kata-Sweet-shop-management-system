from config import params  # Import the 'params' dictionary from your 'config' module


def authenticate_api_key(api_key: str) -> bool:
    """
    Authenticates an API key by comparing it with the pre-configured API key.

    Args:
        api_key (str): The API key provided by the client in the request.

    Returns:
        bool: True if the provided API key matches the configured API_KEY, False otherwise.
    """
    # Compare the provided API key with the expected API_KEY from the configuration parameters.
    return api_key == params["API_KEY"]
