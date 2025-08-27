# app/main.py
from fastapi import FastAPI
from app.db import models
from app.db.session import engine

app = FastAPI(title="Dataset Manager API")

# Crea las tablas si no existen
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"msg": "API lista 🚀"}
