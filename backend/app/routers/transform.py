from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import DatasetResponse
from app.tasks import transform_dataset_task
from celery.result import AsyncResult

router = APIRouter()

@router.post("/transform/{dataset_id}", response_model=dict)
def transform_dataset(dataset_id: int, db: Session = Depends(get_db), operations: dict = {}):
    # Retrieve dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    # Schedule transformation task
    task = transform_dataset_task.delay(dataset.file_path, operations)
    return {"task_id": task.id, "message": "Dataset transformation started."}


@router.get("/transform/status/{task_id}", response_model=dict)
def get_transform_status(task_id: str):
    """Check the status of a dataset transformation task."""
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"task_id": task_id, "status": "Task is pending"}
    elif task_result.state == "SUCCESS":
        return {"task_id": task_id, "status": "Task completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"task_id": task_id, "status": "Task failed", "error": str(task_result.info)}
    else:
        return {"task_id": task_id, "status": task_result.state}
