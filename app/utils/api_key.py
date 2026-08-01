import secrets
import hashlib


def generate_api_key(self)->str:
    """Generate a new API key."""
    return f"sent_live_{secrets.token_urlsafe(32)}"
    
def hash_api_key(self, api_key: str) -> str:
    """Hash the API key using SHA-256."""
    return hashlib.sha256(api_key.encode()).hexdigest()

        