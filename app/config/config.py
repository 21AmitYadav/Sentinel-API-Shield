from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
class Settings:
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("JWT_SECRET")
        self.TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 30))  # Default to 30 minutes if not set
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")  # Default to HS256 if not set


settings = Settings()
