from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext

from youtube_podcast_api.config import get_settings


def verify_google_auth(token: str) -> str:
    try:
        settings = get_settings()

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.google_client_id)

        # ID token is valid. Get the user's Google Account ID from the decoded token and return it
        return idinfo['sub']
    except ValueError:
        # Invalid token, raise the exception
        raise


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_string(string: str) -> str:
    """Hash a string with bcrypt"""
    return context.hash(string)


def verify_hash(plain_string: str, hashed_string: str) -> bool:
    """Verify a string correspond to a hash"""
    return context.verify(plain_string, hashed_string)
