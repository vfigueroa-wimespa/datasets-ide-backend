from sqlalchemy.orm import Session
from app.db.queue_models import GenerationJob
from app.repositories.queue_repo import mark_job_done, mark_job_failed
from app.services.generation_service import generate_and_store_one  # ya existente

def process_claimed_job(db: Session, job: GenerationJob):
    # Tomamos el bot desde el batch
    bot_id = job.batch.bot_id
    # Tu función actual ya espera bot_id y usa GenerationBotConfig internamente
    convo = generate_and_store_one(bot_id, db)
    return convo

def process_job_once(db: Session, job: GenerationJob):
    try:
        _ = process_claimed_job(db, job)
        mark_job_done(db, job.id)
    except Exception as e:
        mark_job_failed(db, job.id, str(e))
