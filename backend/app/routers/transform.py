from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.schemas import DatasetResponse
import pandas as pd

router = APIRouter()

@router.post("/transform/{dataset_id}", response_model=DatasetResponse)
def transform_dataset(dataset_id: int, db: Session = Depends(get_db), operations: dict = {}):
    # Retrieve dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Load dataset
    df = pd.read_csv(dataset.file_path)

    # Apply transformations
    if "drop_columns" in operations:
        df.drop(columns=operations["drop_columns"], inplace=True)
    if "fill_missing" in operations:
        strategy = operations["fill_missing"]
        if strategy == "mean":
            df.fillna(df.mean(), inplace=True)
        elif strategy == "median":
            df.fillna(df.median(), inplace=True)
        else:
            df.fillna(0, inplace=True)
    
    # Save transformed dataset
    transformed_path = dataset.file_path.replace(".csv", "_transformed.csv")
    df.to_csv(transformed_path, index=False)
    dataset.file_path = transformed_path
    db.commit()
    return dataset
