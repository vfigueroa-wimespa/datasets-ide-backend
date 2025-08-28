from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.queue_repo import enqueue_count, batch_progress, claim_next_job
from app.schemas.queue import EnqueueCountIn, EnqueueCountOut, BatchProgress, QueueJobOut
from app.db.queue_models import GenerationJob

router = APIRouter(tags=["Generation Queue"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/bots/{bot_id}/enqueue-count", response_model=EnqueueCountOut)
def enqueue_count_endpoint(bot_id: int, payload: EnqueueCountIn, db: Session = Depends(get_db)):
    try:
        batch_id = enqueue_count(db, bot_id, payload.count, priority=payload.priority)
        return {"batch_id": batch_id, "enqueued": payload.count}
    except ValueError as e:
        raise HTTPException(404, str(e))

@router.get("/batches/{batch_id}/progress", response_model=BatchProgress)
def batch_progress_endpoint(batch_id: int, db: Session = Depends(get_db)):
    stats = batch_progress(db, batch_id)
    if stats["total"] == 0:
        # opcional: 404 si el batch no existe
        raise HTTPException(404, "Batch no encontrado o vacío")
    return stats

# Útil en dev si no corres el worker aparte (manual step)
@router.post("/queue/claim-one", response_model=QueueJobOut)
def claim_one_endpoint(db: Session = Depends(get_db)):
    job = claim_next_job(db)
    if not job:
        raise HTTPException(204, "No hay jobs en cola.")
    return QueueJobOut(
        id=job.id,
        batch_id=job.batch_id,
        status=job.status,
        priority=job.priority,
        attempts=job.attempts,
        error=job.error,
        created_at=job.created_at,
        started_at=job.started_at,
        finished_at=job.finished_at,
    )
