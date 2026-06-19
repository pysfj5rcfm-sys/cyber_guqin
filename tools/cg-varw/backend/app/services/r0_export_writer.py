from __future__ import annotations

import csv
import wave
from datetime import datetime, timezone
from pathlib import Path

from app.config import REVIEW_OUTPUT_ROOT
from app.schemas import ExportReviewRequest, ReviewUnit
from app.services.csv_contract_validator import CSV_REQUIRED_FIELDS, validate_csv_contract
from app.services.export_context_resolver import R0ExportContextResolver


REQUIRED_MARKERS = ("slate_start", "slate_end", "next_slate_start")
R0_CONTEXT_RESOLVER = R0ExportContextResolver()
MANIFEST_REQUIRED_FIELDS = list(CSV_REQUIRED_FIELDS["reviewed_slate_anchor_manifest.csv"])
MARKER_REQUIRED_FIELDS = list(CSV_REQUIRED_FIELDS["raw_marker_review.csv"])
SPLIT_REQUIRED_FIELDS = list(CSV_REQUIRED_FIELDS["split_plan_from_raw_markers.csv"])

MANIFEST_FIELDS = MANIFEST_REQUIRED_FIELDS + [
    "file_id",
    "source_audio",
    "take_id",
    "unit_source",
    "unit_status",
    "boundary_unlinked",
    "is_terminal_take",
    "terminal_boundary_policy",
    "terminal_unit_end_s",
    "terminal_reason",
    "next_slate_marker_source",
    "not_sample_ingest",
    "not_recording_segments",
    "notes",
]

MARKER_FIELDS = MARKER_REQUIRED_FIELDS + [
    "file_id",
    "batch_take_no",
    "script_id",
    "unit_id",
    "source_raw_audio",
    "source_audio",
    "take_id",
    "event_id",
    "event_range",
    "gesture_id",
    "expected_sample_type",
    "unit_status",
    "marker_label_zh",
    "confidence",
    "nudge_total_ms",
    "notes",
    "training_value_class",
    "not_sample_assets",
]

SPLIT_FIELDS = SPLIT_REQUIRED_FIELDS + [
    "file_id",
    "source_audio",
    "take_id",
    "guqin_start_s",
    "expected_sample_type",
    "is_terminal_take",
    "terminal_boundary_policy",
    "terminal_unit_end_s",
    "terminal_reason",
    "next_slate_marker_source",
    "planned_unit_start_s",
    "planned_unit_end_s",
    "planned_clean_start_s",
    "planned_clean_end_s",
    "boundary_unlinked",
    "notes",
    "updated_at",
]


def export_review_csv(request: ExportReviewRequest) -> dict[str, list[str] | str]:
    out_dir = REVIEW_OUTPUT_ROOT / "r0" / "exports" / request.file_id
    out_dir.mkdir(parents=True, exist_ok=True)
    updated_at = datetime.now(timezone.utc).isoformat()
    source_audio = request.source_audio or ""

    manifest_rows = [_manifest_row(request.file_id, source_audio, unit, updated_at) for unit in request.units if unit.unit_status not in {"excluded", "rejected"}]
    marker_rows = [_marker_row(request.file_id, source_audio, unit, marker, updated_at) for unit in request.units for marker in unit.markers]
    split_rows = [_split_row(request.file_id, source_audio, unit, updated_at) for unit in request.units if _is_plannable(unit)]
    contract_warnings = [
        *validate_csv_contract("reviewed_slate_anchor_manifest.csv", manifest_rows),
        *validate_csv_contract("raw_marker_review.csv", marker_rows),
        *validate_csv_contract("split_plan_from_raw_markers.csv", split_rows),
    ]

    files = [
        _write_csv(out_dir / "reviewed_slate_anchor_manifest.csv", MANIFEST_FIELDS, manifest_rows),
        _write_csv(out_dir / "raw_marker_review.csv", MARKER_FIELDS, marker_rows),
        _write_csv(out_dir / "split_plan_from_raw_markers.csv", SPLIT_FIELDS, split_rows),
    ]
    return {"path": str(out_dir), "files": [str(path) for path in files], "contract_warnings": contract_warnings}


def _manifest_row(file_id: str, source_audio: str, unit: ReviewUnit, updated_at: str) -> dict[str, object]:
    times = _marker_times(unit)
    terminal = _terminal_context(source_audio, unit, times)
    review_status = _derive_unit_review_status(unit)
    context = R0_CONTEXT_RESOLVER.resolve(file_id=file_id, source_audio=source_audio, unit=unit).values
    return {
        **context,
        "unit_id": unit.id,
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
        "next_slate_start_s": terminal.get("unit_end_s") if terminal["is_terminal_take"] else times.get("next_slate_start", ""),
        "boundary_unlinked": str(unit.boundary_unlinked).lower(),
        "is_terminal_take": _bool(terminal["is_terminal_take"]),
        "terminal_boundary_policy": terminal["terminal_boundary_policy"],
        "terminal_unit_end_s": terminal.get("unit_end_s", ""),
        "terminal_reason": terminal["terminal_reason"],
        "next_slate_marker_source": terminal["next_slate_marker_source"],
        "review_only": "true",
        "production_grade": "false",
        "not_sample_ingest": "true",
        "not_recording_segments": "true",
        "not_sample_assets": "true",
        "notes": unit.notes,
        "updated_at": updated_at,
    }


def _marker_row(file_id: str, source_audio: str, unit: ReviewUnit, marker, updated_at: str) -> dict[str, object]:
    context = R0_CONTEXT_RESOLVER.resolve(file_id=file_id, source_audio=source_audio, unit=unit).values
    return {
        **context,
        "unit_id": unit.id,
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
        "not_sample_assets": "true",
        "updated_at": updated_at,
    }


def _split_row(file_id: str, source_audio: str, unit: ReviewUnit, updated_at: str) -> dict[str, object]:
    times = _marker_times(unit)
    terminal = _terminal_context(source_audio, unit, times)
    context = R0_CONTEXT_RESOLVER.resolve(file_id=file_id, source_audio=source_audio, unit=unit).values
    unit_start_s = times.get("slate_start", "")
    unit_end_s = terminal.get("unit_end_s") if terminal["is_terminal_take"] else times.get("next_slate_start", "")
    clean_start_s = times.get("guqin_start") or times.get("slate_end", "")
    clean_end_s = unit_end_s
    return {
        **context,
        "unit_id": unit.id,
        "unit_start_s": unit_start_s,
        "unit_end_s": unit_end_s,
        "slate_start_s": times.get("slate_start", ""),
        "slate_end_s": times.get("slate_end", ""),
        "guqin_start_s": times.get("guqin_start", ""),
        "next_slate_start_s": unit_end_s,
        "suggested_clean_start_s": clean_start_s,
        "suggested_clean_end_s": clean_end_s,
        "tail_end_s": times.get("tail_end", ""),
        "split_plan_role": "clean_preview",
        "is_terminal_take": _bool(terminal["is_terminal_take"]),
        "terminal_boundary_policy": terminal["terminal_boundary_policy"],
        "terminal_unit_end_s": terminal.get("unit_end_s", ""),
        "terminal_reason": terminal["terminal_reason"],
        "next_slate_marker_source": terminal["next_slate_marker_source"],
        "planned_unit_start_s": unit_start_s,
        "planned_unit_end_s": unit_end_s,
        "planned_clean_start_s": clean_start_s,
        "planned_clean_end_s": clean_end_s,
        "source_boundary_policy": "reviewed_required_markers",
        "requires_human_confirmation": "true",
        "not_executed": "true",
        "not_recording_segments": "true",
        "not_sample_assets": "true",
        "review_only": "true",
        "production_grade": "false",
        "boundary_unlinked": str(unit.boundary_unlinked).lower(),
        "notes": unit.notes,
        "updated_at": updated_at,
    }


def _marker_times(unit: ReviewUnit) -> dict[str, str]:
    return {marker.key: f"{marker.time:.3f}" for marker in unit.markers}


def _is_plannable(unit: ReviewUnit) -> bool:
    if unit.unit_status in {"excluded", "rejected"}:
        return False
    markers = {marker.key: marker.review_status for marker in unit.markers}
    if _is_terminal_unit(unit, markers):
        return markers.get("slate_start") == "accepted" and markers.get("slate_end") == "accepted"
    return all(markers.get(key) == "accepted" for key in REQUIRED_MARKERS)


def _derive_unit_review_status(unit: ReviewUnit) -> str:
    if unit.unit_status in {"excluded", "rejected"}:
        return "rejected"
    markers = {marker.key: marker for marker in unit.markers}
    marker_statuses = {key: marker.review_status for key, marker in markers.items()}
    if _is_terminal_unit(unit, marker_statuses):
        slate_start = markers.get("slate_start")
        slate_end = markers.get("slate_end")
        if slate_start and slate_end and slate_start.review_status == "accepted" and slate_end.review_status == "accepted":
            return "accepted"
        if any(marker and marker.review_status == "needs_retake" for marker in [slate_start, slate_end]):
            return "needs_retake"
        if any(marker and marker.review_status == "unclear" for marker in [slate_start, slate_end]):
            return "unclear"
        return "candidate"
    required = [markers.get(key) for key in REQUIRED_MARKERS]
    if len(required) == len(REQUIRED_MARKERS) and all(marker and marker.review_status == "accepted" for marker in required):
        return "accepted"
    if any(marker and marker.review_status == "needs_retake" for marker in required):
        return "needs_retake"
    if any(marker and marker.review_status == "unclear" for marker in required):
        return "unclear"
    return "candidate"


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


def _is_terminal_unit(unit: ReviewUnit, marker_statuses: dict[str, str]) -> bool:
    return unit.boundary_type == "file_end" and "next_slate_start" not in marker_statuses


def _terminal_context(source_audio: str, unit: ReviewUnit, times: dict[str, str]) -> dict[str, object]:
    is_terminal = _is_terminal_unit(unit, {marker.key: marker.review_status for marker in unit.markers})
    if not is_terminal:
        return {
            "is_terminal_take": False,
            "terminal_boundary_policy": "",
            "unit_end_s": "",
            "terminal_reason": "",
            "next_slate_marker_source": "reviewed_marker" if times.get("next_slate_start") else "",
        }

    unit_end_s = _raw_duration_s(unit.source_raw_audio or source_audio)
    return {
        "is_terminal_take": True,
        "terminal_boundary_policy": "raw_end",
        "unit_end_s": unit_end_s,
        "terminal_reason": "no_next_slate_in_batch",
        "next_slate_marker_source": "terminal_raw_end",
    }


def _raw_duration_s(source_audio: str) -> str:
    path = _resolve_audio_path(source_audio)
    with wave.open(str(path), "rb") as handle:
        duration_s = handle.getnframes() / handle.getframerate()
    return f"{duration_s:.6f}"


def _resolve_audio_path(source_audio: str) -> Path:
    path = Path(source_audio)
    if path.is_file():
        return path
    for parent in [Path.cwd(), *Path.cwd().parents]:
        candidate = parent / source_audio
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"Unable to resolve terminal raw audio path: {source_audio}")


def _bool(value: object) -> str:
    return str(bool(value)).lower()
