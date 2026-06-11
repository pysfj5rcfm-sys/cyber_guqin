from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import REVIEW_OUTPUT_ROOT
from app.schemas import SaveReviewRequest
from app.services.review_unit_builder import draft_path


def save_review_draft(request: SaveReviewRequest) -> dict[str, Any]:
    path = draft_path(request.file_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "file_id": request.file_id,
        "source_audio": request.source_audio,
        "notes": request.notes,
        "units": [unit.model_dump() for unit in request.units],
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "review_only": True,
        "production_grade": False,
        "not_sample_ingest": True,
        "not_recording_segments": True,
        "not_sample_assets": True,
    }
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {"path": str(path), "payload": payload}


def review_output_root() -> Path:
    return REVIEW_OUTPUT_ROOT
