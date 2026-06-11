from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from app.config import REVIEW_OUTPUT_ROOT
from app.schemas import ExportReviewRequest, ReviewUnit


REQUIRED_MARKERS = ("slate_start", "slate_end", "next_slate_start")

MANIFEST_FIELDS = [
    "file_id",
    "source_audio",
    "unit_id",
    "recording_take_no",
    "batch_take_no",
    "unit_source",
    "unit_status",
    "review_status",
    "event_id",
    "event_range",
    "gesture_id",
    "expected_sample_type",
    "slate_start_s",
    "slate_end_s",
    "guqin_start_s",
    "tail_end_s",
    "next_slate_start_s",
    "boundary_unlinked",
    "review_only",
    "production_grade",
    "not_sample_ingest",
    "not_recording_segments",
    "not_sample_assets",
    "notes",
    "updated_at",
]

MARKER_FIELDS = [
    "file_id",
    "source_audio",
    "unit_id",
    "recording_take_no",
    "unit_status",
    "marker_id",
    "marker_type",
    "marker_label_zh",
    "time_s",
    "source",
    "confidence",
    "review_status",
    "nudge_total_ms",
    "notes",
    "review_only",
    "production_grade",
    "training_value_class",
    "updated_at",
]

SPLIT_FIELDS = [
    "file_id",
    "source_audio",
    "unit_id",
    "recording_take_no",
    "batch_take_no",
    "planned_unit_start_s",
    "planned_unit_end_s",
    "planned_clean_start_s",
    "planned_clean_end_s",
    "source_boundary_policy",
    "requires_human_confirmation",
    "not_executed",
    "not_recording_segments",
    "not_sample_assets",
    "review_only",
    "production_grade",
    "notes",
]


def export_review_csv(request: ExportReviewRequest) -> dict[str, list[str] | str]:
    out_dir = REVIEW_OUTPUT_ROOT / "r0" / "exports" / request.file_id
    out_dir.mkdir(parents=True, exist_ok=True)
    updated_at = datetime.now(timezone.utc).isoformat()
    source_audio = request.source_audio or ""

    manifest_rows = [_manifest_row(request.file_id, source_audio, unit, updated_at) for unit in request.units if unit.unit_status not in {"excluded", "rejected"}]
    marker_rows = [_marker_row(request.file_id, source_audio, unit, marker, updated_at) for unit in request.units for marker in unit.markers]
    split_rows = [_split_row(request.file_id, source_audio, unit) for unit in request.units if _is_plannable(unit)]

    files = [
        _write_csv(out_dir / "reviewed_slate_anchor_manifest.csv", MANIFEST_FIELDS, manifest_rows),
        _write_csv(out_dir / "raw_marker_review.csv", MARKER_FIELDS, marker_rows),
        _write_csv(out_dir / "split_plan_from_raw_markers.csv", SPLIT_FIELDS, split_rows),
    ]
    return {"path": str(out_dir), "files": [str(path) for path in files]}


def _manifest_row(file_id: str, source_audio: str, unit: ReviewUnit, updated_at: str) -> dict[str, object]:
    times = _marker_times(unit)
    review_status = _derive_unit_review_status(unit)
    return {
        "file_id": file_id,
        "source_audio": source_audio,
        "unit_id": unit.id,
        "recording_take_no": unit.recording_take_no or unit.takeId,
        "batch_take_no": unit.batch_take_no or str(unit.sequence),
        "unit_source": unit.source,
        "unit_status": _derive_unit_status(unit),
        "review_status": review_status,
        "event_id": unit.event_id,
        "event_range": unit.event_range,
        "gesture_id": unit.gesture_id,
        "expected_sample_type": unit.expected_sample_type,
        "slate_start_s": times.get("slate_start", ""),
        "slate_end_s": times.get("slate_end", ""),
        "guqin_start_s": times.get("guqin_start", ""),
        "tail_end_s": times.get("tail_end", ""),
        "next_slate_start_s": times.get("next_slate_start", ""),
        "boundary_unlinked": str(unit.boundary_unlinked).lower(),
        "review_only": "true",
        "production_grade": "false",
        "not_sample_ingest": "true",
        "not_recording_segments": "true",
        "not_sample_assets": "true",
        "notes": unit.notes,
        "updated_at": updated_at,
    }


def _marker_row(file_id: str, source_audio: str, unit: ReviewUnit, marker, updated_at: str) -> dict[str, object]:
    return {
        "file_id": file_id,
        "source_audio": source_audio,
        "unit_id": unit.id,
        "recording_take_no": unit.recording_take_no or unit.takeId,
        "unit_status": _derive_unit_status(unit),
        "marker_id": marker.id or f"{unit.id}:{marker.key}",
        "marker_type": marker.key,
        "marker_label_zh": marker.label,
        "time_s": f"{marker.time:.3f}",
        "source": marker.source or unit.source,
        "confidence": "" if marker.confidence is None else marker.confidence,
        "review_status": marker.review_status,
        "nudge_total_ms": marker.nudge_total_ms,
        "notes": marker.notes,
        "review_only": "true",
        "production_grade": "false",
        "training_value_class": "review_only_boundary_draft",
        "updated_at": updated_at,
    }


def _split_row(file_id: str, source_audio: str, unit: ReviewUnit) -> dict[str, object]:
    times = _marker_times(unit)
    return {
        "file_id": file_id,
        "source_audio": source_audio,
        "unit_id": unit.id,
        "recording_take_no": unit.recording_take_no or unit.takeId,
        "batch_take_no": unit.batch_take_no or str(unit.sequence),
        "planned_unit_start_s": times.get("slate_start", ""),
        "planned_unit_end_s": times.get("next_slate_start", ""),
        "planned_clean_start_s": times.get("guqin_start") or times.get("slate_end", ""),
        "planned_clean_end_s": times.get("next_slate_start", ""),
        "source_boundary_policy": "reviewed_required_markers",
        "requires_human_confirmation": "true",
        "not_executed": "true",
        "not_recording_segments": "true",
        "not_sample_assets": "true",
        "review_only": "true",
        "production_grade": "false",
        "notes": unit.notes,
    }


def _marker_times(unit: ReviewUnit) -> dict[str, str]:
    return {marker.key: f"{marker.time:.3f}" for marker in unit.markers}


def _is_plannable(unit: ReviewUnit) -> bool:
    if unit.unit_status in {"excluded", "rejected"}:
        return False
    markers = {marker.key: marker.review_status for marker in unit.markers}
    return all(markers.get(key) == "accepted" for key in REQUIRED_MARKERS)


def _derive_unit_review_status(unit: ReviewUnit) -> str:
    if unit.unit_status in {"excluded", "rejected"}:
        return "rejected"
    markers = {marker.key: marker for marker in unit.markers}
    required = [markers.get(key) for key in REQUIRED_MARKERS]
    if len(required) == len(REQUIRED_MARKERS) and all(marker and marker.review_status == "accepted" for marker in required):
        return "accepted"
    if any(marker and marker.review_status == "needs_retake" for marker in required):
        return "needs_retake"
    if any(marker and marker.review_status == "unclear" for marker in required):
        return "unclear"
    if any((marker.review_status and marker.review_status != "candidate") or marker.nudge_total_ms for marker in unit.markers):
        return "in_progress"
    return "not_started"


def _derive_unit_status(unit: ReviewUnit) -> str:
    if unit.unit_status in {"excluded", "rejected"}:
        return unit.unit_status
    review_status = _derive_unit_review_status(unit)
    if review_status == "accepted":
        return "confirmed"
    if review_status == "needs_retake":
        return "needs_retake"
    if review_status == "not_started":
        return "candidate"
    return "needs_review"


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> Path:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path
