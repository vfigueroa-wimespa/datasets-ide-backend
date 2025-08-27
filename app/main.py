from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import models
from app.db import generation_models  # 👈 nuevo
from app.db.session import engine
from app.routes import dataset_routes, conversation_routes, message_routes, generation_bot_routes
from app.routes import generation_test_routes

app = FastAPI(title="Dataset Manager API")

# --- CORS ---
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # or ["*"] para desarrollo libre
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB init ---
models.Base.metadata.create_all(bind=engine)
generation_models.Base.metadata.create_all(bind=engine)

# --- Routes ---
app.include_router(dataset_routes.router)
app.include_router(conversation_routes.router)
app.include_router(message_routes.router)
app.include_router(generation_bot_routes.router)  # 👈 nuevo
app.include_router(generation_test_routes.router)  # 👈 nuevo

@app.get("/")
def read_root():
    return {"msg": "API lista 🚀"}
