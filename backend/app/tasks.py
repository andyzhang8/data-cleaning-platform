from celery import Celery
from app.config import settings
from app.services.cleaning import drop_columns, fill_missing_values, normalize_columns, detect_outliers
import pandas as pd
import os

# Initialize Celery
celery_app = Celery(
    "tasks",
    broker=settings.REDIS_URL,  
    backend=settings.REDIS_URL,  
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Only accept JSON-serialized tasks
    result_serializer="json",
)

@celery_app.task
def transform_dataset_task(dataset_path: str, operations: dict) -> str:
    """Perform dataset transformations asynchronously."""
    try:
        # Load dataset
        df = pd.read_csv(dataset_path)

        # Apply transformations
        if "drop_columns" in operations:
            df = drop_columns(df, operations["drop_columns"])
        if "fill_missing" in operations:
            df = fill_missing_values(df, operations["fill_missing"])
        if "normalize_columns" in operations:
            df = normalize_columns(df, operations["normalize_columns"])
        if "detect_outliers" in operations:
            df = detect_outliers(df, operations["detect_outliers"])

        # Save transformed dataset
        transformed_path = dataset_path.replace(".csv", "_transformed.csv")
        df.to_csv(transformed_path, index=False)
        return transformed_path
    except Exception as e:
        return f"Task failed: {e}"

@celery_app.task
def cleanup_temp_files_task(directory: str):
    """Clean up temp files asynchronously."""
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        return f"Task failed: {e}"
