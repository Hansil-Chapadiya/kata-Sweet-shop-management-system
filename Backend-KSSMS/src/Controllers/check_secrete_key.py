from config import params

def authenticate_api_key(api_key):
    return api_key == params['API_KEY']