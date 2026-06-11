from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.config import REVIEW_OUTPUT_ROOT
from app.schemas import Marker, ReviewUnit
from app.services.asr_candidate_loader import load_asr_candidates


MARKER_COLORS = {
    "slate_start": "green",
    "slate_end": "blue",
    "guqin_start": "gold",
    "tail_end": "purple",
    "next_slate_start": "cyan",
}

MARKER_LABEL_ZH = {
    "slate_start": "口播起始",
    "slate_end": "口播结束",
    "guqin_start": "古琴起声",
    "tail_end": "尾音结束",
    "next_slate_start": "下一口播起始",
}


def draft_path(file_id: str) -> Path:
    return REVIEW_OUTPUT_ROOT / "r0" / "drafts" / f"{file_id}.raw_marker_review.json"


def load_or_build_review_units(file_id: str, raw_path: Path) -> dict[str, Any]:
    path = draft_path(file_id)
    if path.exists():
        with path.open("r", encoding="utf-8-sig") as handle:
            return json.load(handle)

    candidates_data = load_asr_candidates(raw_path)
    units = build_units_from_candidates(candidates_data.get("candidates", []))
    return {
        "file_id": file_id,
        "source_audio": raw_path.name,
        "source": "asr_candidates" if units else "manual_empty",
        "message": "" if units else "未找到 ASR 候选，可手动新增 T",
        "units": [unit.model_dump() for unit in units],
        "review_only": True,
        "production_grade": False,
        "not_sample_ingest": True,
        "not_recording_segments": True,
        "not_sample_assets": True,
    }


def build_units_from_candidates(candidates: list[Any]) -> list[ReviewUnit]:
    units: list[ReviewUnit] = []
    for index, candidate in enumerate(candidates, start=1):
        if not isinstance(candidate, dict):
            continue
        unit_id = str(candidate.get("unit_id") or candidate.get("id") or f"T{index:03d}")
        markers_obj = candidate.get("markers") if isinstance(candidate.get("markers"), dict) else candidate
        boundary = candidate.get("boundary") if isinstance(candidate.get("boundary"), dict) else {}
        boundary_type = boundary.get("type") if boundary.get("type") in {"next_slate_start", "file_end"} else "next_slate_start"
        markers = []
        for key in ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"]:
            if key not in markers_obj:
                continue
            markers.append(
                Marker(
                    key=key,
                    label=MARKER_LABEL_ZH[key],
                    time=float(markers_obj[key]),
                    color=MARKER_COLORS[key],
                    source="asr_candidate",
                    confidence=_float_or_none(candidate.get("confidence")),
                    review_status="candidate",
                )
            )
        units.append(
            ReviewUnit(
                id=unit_id,
                sequence=int(candidate.get("sequence") or index),
                unit_status="candidate",
                review_status="not_started",
                source="asr_candidate",
                takeId=str(candidate.get("take_id") or f"TAKE_{unit_id}"),
                boundary_type=boundary_type,
                markers=markers,
            )
        )
    return units


def _float_or_none(value: Any) -> float | None:
    try:
        return None if value in {None, ""} else float(value)
    except (TypeError, ValueError):
        return None
