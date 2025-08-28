# app/core/worker.py
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import SessionLocal
from app.repositories.queue_repo import claim_next_job
from app.services.queue_service import process_job_once

POLL_INTERVAL_SEC = 1.5

async def _worker_loop(stop_event: asyncio.Event):
    """
    Worker secuencial: toma 1 job por vez.
    Corre en un task de background propio de FastAPI.
    """
    while not stop_event.is_set():
        db = SessionLocal()
        try:
            job = claim_next_job(db)  # sync DB call
            if not job:
                await asyncio.sleep(POLL_INTERVAL_SEC)
                continue

            # Procesamos el job de forma secuencial.
            # Como process_job_once es blocking/sync (I/O a modelo, DB),
            # lo empujamos a un thread para no bloquear el event loop.
            await asyncio.to_thread(process_job_once, db, job)

        except Exception as e:
            # En un worker robusto loggearías a logger
            # y eventualmente métricas. Aquí lo simplificamos.
            # print(f"[worker] error: {e}")
            pass
        finally:
            db.close()

@asynccontextmanager
async def queue_lifespan(app: FastAPI):
    """
    Lifespan que crea/detiene el worker al iniciar/cerrar la app.
    Garantiza 1 sola instancia.
    """
    stop_event = asyncio.Event()
    app.state.queue_stop_event = stop_event
    app.state.queue_task = asyncio.create_task(_worker_loop(stop_event))
    try:
        yield
    finally:
        stop_event.set()
        # Cancelamos con timeout suave
        try:
            await asyncio.wait_for(app.state.queue_task, timeout=5.0)
        except asyncio.TimeoutError:
            app.state.queue_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await app.state.queue_task
