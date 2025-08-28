# app/services/dataset_export_service.py
import json
from fastapi.responses import StreamingResponse
from io import BytesIO

def export_dataset_to_jsonl(dataset_data: dict):
    buffer = BytesIO()
    for conv in dataset_data["conversations"]:
        line = {"conversations": conv}
        buffer.write((json.dumps(line, ensure_ascii=False) + "\n").encode("utf-8"))
    buffer.seek(0)
    return buffer

def get_jsonl_response(buffer, filename="dataset.jsonl"):
    return StreamingResponse(
        buffer,
        media_type="application/jsonl",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
