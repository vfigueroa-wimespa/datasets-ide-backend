# Zenomy Dataset Manager 🧠

Una plataforma interna para la creación, visualización y gestión de datasets conversacionales para fine-tuning de modelos LLM.

## 🚀 Tecnologías
- Python + FastAPI
- SQLAlchemy + SQLite (dev)
- Organización modular: `app/`, `data/`, `schemas/`, `routes/`, etc.

## 🛠️ Instalación

```bash
git clone https://github.com/zenomy-labs/dataset-manager.git
cd dataset-manager
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
