from dotenv import load_dotenv, set_key
import os
import secrets
import json
from pydantic import BaseSettings, Field
from typing import List

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT settings
    PRIMARY_SECRET_KEY: str = os.getenv("PRIMARY_SECRET_KEY", secrets.token_hex(32))
    PREVIOUS_SECRET_KEYS: List[str] = Field(default_factory=lambda: eval(
        os.getenv("PREVIOUS_SECRET_KEYS", "[]")
    ))
    AUTHJWT_SECRET_KEY: str = os.getenv("AUTHJWT_SECRET_KEY", "your_secret_key_here")  # Add this

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # File settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "temp/uploads")
    ALLOWED_FILE_TYPES: List[str] = eval(
        os.getenv("ALLOWED_FILE_TYPES", "['text/csv', 'application/vnd.ms-excel', 'application/json']")
    )
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))

    def rotate_secret_key(self):
        """Generate a new secret key, update settings, and persist to .env."""
        new_key = secrets.token_hex(32)
        if self.PRIMARY_SECRET_KEY not in self.PREVIOUS_SECRET_KEYS:
            self.PREVIOUS_SECRET_KEYS.append(self.PRIMARY_SECRET_KEY)

        self.PRIMARY_SECRET_KEY = new_key

        # Persist changes to .env file
        set_key(dotenv_path, "PRIMARY_SECRET_KEY", self.PRIMARY_SECRET_KEY)
        set_key(dotenv_path, "PREVIOUS_SECRET_KEYS", json.dumps(self.PREVIOUS_SECRET_KEYS))

        print(f"Secret key rotated. New primary key: {new_key}")


# Init
settings = Settings()

if __name__ == "__main__":
    # Debugging
    print("Before rotation:")
    print("JWT Primary Secret Key:", settings.PRIMARY_SECRET_KEY)
    print("JWT Previous Secret Keys:", settings.PREVIOUS_SECRET_KEYS)

    # Rotate the key
    settings.rotate_secret_key()

    print("After rotation:")
    print("JWT Primary Secret Key:", settings.PRIMARY_SECRET_KEY)
    print("JWT Previous Secret Keys:", settings.PREVIOUS_SECRET_KEYS)
