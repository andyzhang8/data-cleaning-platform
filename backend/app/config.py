from pydantic import BaseSettings
from typing import List
import secrets
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str

    # Redis settings for Celery
    REDIS_URL: str

    # JWT settings
    PRIMARY_SECRET_KEY: str  # Current primary secret key
    PREVIOUS_SECRET_KEYS: List[str] = []  # List of previous keys
    ALGORITHM: str = "HS256"  # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in minutes

    # File settings
    UPLOAD_DIR: str = "temp/uploads"  # Directory for temporary storage
    ALLOWED_FILE_TYPES: List[str] = ["text/csv", "application/vnd.ms-excel", "application/json"]
    MAX_UPLOAD_SIZE_MB: int = 50  # in MB

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../.env")
        env_file_encoding = "utf-8"

    def rotate_secret_key(self):
        """Generate a new secret key and update the settings."""
        new_key = secrets.token_hex(32)
        if self.PRIMARY_SECRET_KEY not in self.PREVIOUS_SECRET_KEYS:
            self.PREVIOUS_SECRET_KEYS.append(self.PRIMARY_SECRET_KEY)
        self.PRIMARY_SECRET_KEY = new_key
        print(f"Secret key rotated. New primary key: {new_key}")

# Initialize settings
settings = Settings()

if __name__ == "__main__":
    # For debugging
    print("Database URL:", settings.DATABASE_URL)
    print("Redis URL:", settings.REDIS_URL)
    print("JWT Primary Secret Key:", settings.PRIMARY_SECRET_KEY)
    print("JWT Previous Secret Keys:", settings.PREVIOUS_SECRET_KEYS)
    print("Upload Directory:", settings.UPLOAD_DIR)
    print("Allowed File Types:", settings.ALLOWED_FILE_TYPES)
    print("Max Upload Size (MB):", settings.MAX_UPLOAD_SIZE_MB)

    # Rotate the key for testing
    settings.rotate_secret_key()
