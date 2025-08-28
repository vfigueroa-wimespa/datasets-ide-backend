# app/routes/dataset_export_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.dataset_repository import get_dataset_with_conversations
from app.services.dataset_export_service import export_dataset_to_jsonl, get_jsonl_response

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/{dataset_id}/export")
def export_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset_data = get_dataset_with_conversations(db, dataset_id)
    if not dataset_data:
        raise HTTPException(status_code=404, detail="Dataset not found")

    buffer = export_dataset_to_jsonl(dataset_data)
    return get_jsonl_response(buffer, f"{dataset_data['name']}.jsonl")
