import os
from app.config import settings

def generate_file_path(file_name: str) -> str:
    """Generate a unique file path for storing datasets."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    return os.path.join(settings.UPLOAD_DIR, file_name)

def validate_file_size(file: bytes) -> bool:
    """Validate that the uploaded file does not exceed the maximum size."""
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024  # Convert MB to bytes
    return len(file) <= max_size

def clean_temp_files(directory: str):
    """Remove temporary files in a given directory."""
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
