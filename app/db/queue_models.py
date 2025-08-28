# app/db/queue_models.py
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, ForeignKey, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class GenerationBatch(Base):
    __tablename__ = "generation_batches"

    id = Column(Integer, primary_key=True)
    # Referencia al bot que ya tiene system_prompt, temperature, max_turns, etc.
    bot_id = Column(
        Integer,
        ForeignKey("generation_bot_configs.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    jobs = relationship(
        "GenerationJob",
        back_populates="batch",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True)
    batch_id = Column(
        Integer,
        ForeignKey("generation_batches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Cola
    status = Column(String(16), nullable=False, default="queued")  # queued|running|done|failed
    priority = Column(Integer, nullable=False, default=100)
    attempts = Column(Integer, nullable=False, default=0)

    # Trazabilidad (sin prompt/meta: eso está en GenerationBotConfig)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    batch = relationship("GenerationBatch", back_populates="jobs")

# Índices útiles (FIFO por prioridad y fecha + filtros por estado)
Index(
    "ix_generation_jobs_status_priority_created",
    GenerationJob.status, GenerationJob.priority, GenerationJob.created_at
)
Index(
    "ix_generation_jobs_status_created",
    GenerationJob.status, GenerationJob.created_at
)
