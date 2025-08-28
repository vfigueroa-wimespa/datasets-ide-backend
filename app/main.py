# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Lifespan con worker de la cola ---
from app.workers.generation_worker import queue_lifespan  # <- usa el background worker (startup/shutdown)

# --- DB init ---
# Importa TODOS los modelos antes de crear tablas
from app.db import models
from app.db import generation_models
from app.db import queue_models
from app.db.session import engine
from app.db.base import Base  # Base común

# --- Rutas ---
from app.routes import (
    dataset_routes,
    conversation_routes,
    message_routes,
    generation_bot_routes,
    generation_test_routes,  # opcional, tu endpoint de prueba sync
    generation_queue,        # encolar y progreso de batches
)

app = FastAPI(
    title="Dataset Manager API",
    lifespan=queue_lifespan,   # <-- aquí activamos el worker de fondo
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # en prod: lista específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Crear tablas (una sola pasada) ---
# Nota: como todos tus modelos comparten la misma Base, basta con una llamada,
# siempre que importes los módulos que definen los modelos ANTES.
Base.metadata.create_all(bind=engine)

# --- Rutas ---
app.include_router(dataset_routes.router)
app.include_router(conversation_routes.router)
app.include_router(message_routes.router)
app.include_router(generation_bot_routes.router)
app.include_router(generation_test_routes.router)  # opcional
app.include_router(generation_queue.router)

@app.get("/")
def read_root():
    return {"msg": "API lista 🚀"}

# Health simple del worker (útil para ver si está vivo)
@app.get("/queue/status")
def queue_status():
    task = getattr(app.state, "queue_task", None)
    running = bool(task and not task.done())
    return {"worker_running": running}
