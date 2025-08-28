from datetime import datetime, timedelta
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session, joinedload
from app.db.queue_models import GenerationBatch, GenerationJob
from app.db.generation_models import GenerationBotConfig  # si lo tienes en otro módulo, ajusta el import

# 1) Encolar N jobs para un bot
def enqueue_count(db: Session, bot_id: int, count: int, priority: int = 100) -> int:
    # Validamos que el bot exista
    bot = db.get(GenerationBotConfig, bot_id)
    if not bot:
        raise ValueError(f"Bot {bot_id} no existe")

    batch = GenerationBatch(bot_id=bot_id)
    db.add(batch)
    db.flush()  # tener batch.id

    rows = [GenerationJob(batch_id=batch.id, status="queued", priority=priority) for _ in range(count)]
    db.add_all(rows)
    db.commit()
    return batch.id

# 2) Reclamar el siguiente job (FIFO por priority, created_at)
# Compatible con SQLite (sin SELECT FOR UPDATE)
def claim_next_job(db: Session):
    upd = text("""
    UPDATE generation_jobs
       SET status='running', attempts=attempts+1, started_at=:now
     WHERE id IN (
        SELECT id FROM generation_jobs
         WHERE status='queued'
         ORDER BY priority ASC, created_at ASC
         LIMIT 1
     )
    """)
    res = db.execute(upd, {"now": datetime.utcnow()})
    if res.rowcount == 0:
        db.commit()
        return None

    job = db.execute(
        select(GenerationJob)
        .options(joinedload(GenerationJob.batch))
        .where(GenerationJob.status == "running")
        .order_by(GenerationJob.started_at.asc())
        .limit(1)
    ).scalar_one_or_none()
    db.commit()
    return job

def mark_job_done(db: Session, job_id: int):
    db.execute(
        text("UPDATE generation_jobs SET status='done', finished_at=:now WHERE id=:id"),
        {"now": datetime.utcnow(), "id": job_id},
    )
    db.commit()

def mark_job_failed(db: Session, job_id: int, error_msg: str):
    db.execute(
        text("""UPDATE generation_jobs
                   SET status='failed', error=:err, finished_at=:now
                 WHERE id=:id"""),
        {"now": datetime.utcnow(), "id": job_id, "err": (error_msg or "")[:2000]},
    )
    db.commit()

# (Opcional) watchdog: resetear jobs trabados
def reset_stuck_jobs(db: Session, older_than_minutes: int = 30, max_attempts: int = 3):
    cutoff = datetime.utcnow() - timedelta(minutes=older_than_minutes)
    db.execute(
        text("""
        UPDATE generation_jobs
           SET status='queued', started_at=NULL
         WHERE status='running'
           AND started_at < :cutoff
           AND attempts < :max_attempts
        """),
        {"cutoff": cutoff, "max_attempts": max_attempts},
    )
    db.commit()

def batch_progress(db: Session, batch_id: int) -> dict:
    total = db.query(func.count(GenerationJob.id)).filter(GenerationJob.batch_id == batch_id).scalar() or 0
    count_by = (
        db.query(GenerationJob.status, func.count(GenerationJob.id))
          .filter(GenerationJob.batch_id == batch_id)
          .group_by(GenerationJob.status)
          .all()
    )
    stats = {"queued": 0, "running": 0, "done": 0, "failed": 0}
    for status, n in count_by:
        stats[status] = n
    stats["total"] = total
    stats["batch_id"] = batch_id
    return stats
