from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import Dataset, DatasetCreate, DatasetResponse
import os
from app.config import settings

router = APIRouter()

@router.post("/upload", response_model=DatasetResponse)
def upload_dataset(name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save file
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    # Store dataset metadata
    dataset = Dataset(name=name, file_path=file_path)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset
