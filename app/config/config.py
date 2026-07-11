from dotenv import load_dotenv
import os


class Settings:
    load_dotenv()  # Load environment variables from .env file
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("JWT_SECRET")


settings = Settings()
print(settings.DATABASE_URL)
print(settings.SECRET_KEY)