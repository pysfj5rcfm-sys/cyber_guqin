from __future__ import annotations

import csv
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

    exported = load_units_from_exported_csv(file_id, raw_path)
    if exported:
        return exported

    candidates_data = load_asr_candidates(raw_path)
    units = build_units_from_candidates(candidates_data.get("candidates", []), source_raw_audio=raw_path.name)
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


def load_units_from_exported_csv(file_id: str, raw_path: Path) -> dict[str, Any] | None:
    csv_path = exported_marker_review_path(file_id)
    if not csv_path:
        return None
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("file_id") == file_id or not row.get("file_id")]
    if not rows:
        return None
    units = build_units_from_export_rows(rows, source_raw_audio=raw_path.name)
    if not units:
        return None
    return {
        "file_id": file_id,
        "source_audio": raw_path.name,
        "source": "exported_csv",
        "message": f"已从工程目录导出 CSV 恢复 R0 初始状态：{csv_path}",
        "units": [unit.model_dump() for unit in units],
        "review_only": True,
        "production_grade": False,
        "not_sample_ingest": True,
        "not_recording_segments": True,
        "not_sample_assets": True,
    }


def exported_marker_review_path(file_id: str) -> Path | None:
    direct = REVIEW_OUTPUT_ROOT / "r0" / "exports" / file_id / "raw_marker_review.csv"
    if direct.exists():
        return direct
    export_root = REVIEW_OUTPUT_ROOT / "r0" / "exports"
    if not export_root.exists():
        return None
    for candidate in sorted(export_root.glob("*/raw_marker_review.csv"), reverse=True):
        if candidate.exists():
            return candidate
    return None


def build_units_from_export_rows(rows: list[dict[str, str]], source_raw_audio: str = "") -> list[ReviewUnit]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        unit_id = row.get("unit_id") or row.get("id")
        marker_type = row.get("marker_type")
        if not unit_id or marker_type not in MARKER_LABEL_ZH:
            continue
        grouped.setdefault(unit_id, []).append(row)

    units: list[ReviewUnit] = []
    for index, (unit_id, marker_rows) in enumerate(sorted(grouped.items()), start=1):
        first = marker_rows[0]
        markers = []
        for row in sorted(marker_rows, key=lambda item: marker_order(item.get("marker_type", ""))):
            marker_type = row.get("marker_type", "")
            if marker_type not in MARKER_LABEL_ZH:
                continue
            markers.append(
                Marker(
                    key=marker_type,
                    label=row.get("marker_label_zh") or MARKER_LABEL_ZH[marker_type],
                    time=_float_or_default(row.get("time_s"), 0.0),
                    color=MARKER_COLORS[marker_type],
                    source=row.get("source") or "exported_csv",
                    confidence=_float_or_none(row.get("confidence")),
                    review_status=row.get("review_status") or "candidate",
                    nudge_total_ms=_int_or_default(row.get("nudge_total_ms"), 0),
                    notes=row.get("notes", ""),
                )
            )
        units.append(
            ReviewUnit(
                id=unit_id,
                sequence=_int_or_default(first.get("sequence"), index),
                unit_status=first.get("unit_status") or "needs_review",
                review_status=first.get("review_status") or "not_started",
                source="exported_csv",
                takeId=first.get("take_id") or f"TAKE_{unit_id}",
                boundary_type=first.get("boundary_type") if first.get("boundary_type") in {"next_slate_start", "file_end"} else "next_slate_start",
                boundary_unlinked=_bool_from_text(first.get("boundary_unlinked")),
                notes=first.get("unit_notes") or first.get("notes") or "",
                recording_session_id=first.get("recording_session_id", ""),
                recording_id=first.get("recording_id", ""),
                piece_id=first.get("piece_id", ""),
                qinist_id=first.get("qinist_id", ""),
                batch_id=first.get("batch_id", ""),
                recording_take_no=first.get("recording_take_no", ""),
                batch_take_no=first.get("batch_take_no", ""),
                script_id=first.get("script_id", ""),
                source_raw_audio=first.get("source_raw_audio") or source_raw_audio,
                event_id=first.get("event_id", ""),
                event_range=first.get("event_range", ""),
                gesture_id=first.get("gesture_id", ""),
                expected_sample_type=first.get("expected_sample_type", ""),
                markers=markers,
            )
        )
    return units


def build_units_from_candidates(candidates: list[Any], source_raw_audio: str = "") -> list[ReviewUnit]:
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
                recording_session_id=str(candidate.get("recording_session_id") or ""),
                recording_id=str(candidate.get("recording_id") or ""),
                piece_id=str(candidate.get("piece_id") or ""),
                qinist_id=str(candidate.get("qinist_id") or ""),
                batch_id=str(candidate.get("batch_id") or ""),
                recording_take_no=str(candidate.get("recording_take_no") or ""),
                batch_take_no=str(candidate.get("batch_take_no") or ""),
                script_id=str(candidate.get("script_id") or ""),
                source_raw_audio=str(candidate.get("source_raw_audio") or candidate.get("audio_file") or source_raw_audio),
                event_id=str(candidate.get("event_id") or ""),
                event_range=str(candidate.get("event_range") or ""),
                gesture_id=str(candidate.get("gesture_id") or ""),
                expected_sample_type=str(candidate.get("expected_sample_type") or ""),
                markers=markers,
            )
        )
    return units


def _float_or_none(value: Any) -> float | None:
    try:
        return None if value in {None, ""} else float(value)
    except (TypeError, ValueError):
        return None


def _float_or_default(value: Any, default: float) -> float:
    parsed = _float_or_none(value)
    return default if parsed is None else parsed


def _int_or_default(value: Any, default: int) -> int:
    try:
        return default if value in {None, ""} else int(float(value))
    except (TypeError, ValueError):
        return default


def _bool_from_text(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def marker_order(marker_type: str) -> int:
    return ["slate_start", "slate_end", "guqin_start", "tail_end", "next_slate_start"].index(marker_type) if marker_type in MARKER_LABEL_ZH else 99
