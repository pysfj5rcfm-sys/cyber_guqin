from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import REVIEW_OUTPUT_ROOT
from app.schemas import R1DraftResponse, R1Marker, R1ReviewExportRequest, R1ReviewSaveRequest, SplitSegment


RENDER_ANCHOR_FIELDS = [
    "batch_id",
    "take_id",
    "segment_id",
    "source_audio",
    "event_id",
    "event_range",
    "variant",
    "pre_idle_end_s",
    "gesture_start_s",
    "render_anchor_s",
    "tail_end_s",
    "anchor_type",
    "pre_attack_music_policy",
    "tail_policy",
    "render_usable",
    "review_status",
    "review_only",
    "production_grade",
    "not_sample_assets",
    "not_render_executed",
    "updated_at",
    "notes",
]

MARKER_REVIEW_FIELDS = [
    "batch_id",
    "take_id",
    "segment_id",
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

SEGMENT_QC_FIELDS = [
    "batch_id",
    "take_id",
    "segment_id",
    "source_audio",
    "duration_s",
    "render_usable",
    "reference_only",
    "unclear",
    "needs_retake",
    "rejected",
    "reject_reason",
    "noise_issue",
    "click_issue",
    "tail_clipped",
    "attack_clipped",
    "slate_residue",
    "wrong_take",
    "notes",
    "review_only",
    "production_grade",
    "not_sample_assets",
    "not_render_executed",
    "updated_at",
]


def save_r1_draft(request: R1ReviewSaveRequest) -> dict[str, Any]:
    updated_at = datetime.now(timezone.utc).isoformat()
    out_path = _draft_path(request.batch_id)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    segments = [with_derived_state(segment) for segment in request.segments]
    payload = {
        "batch_id": request.batch_id,
        "notes": request.notes,
        "segments": [segment.model_dump() for segment in segments],
        "change_log": [_change_log_row(segment) for segment in segments],
        "updated_at": updated_at,
        "review_only": True,
        "production_grade": False,
        "not_sample_assets": True,
        "not_render_executed": True,
        "not_ml_training_data": True,
    }
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {"path": str(out_path), "payload": payload}


def load_r1_draft(batch_id: str) -> R1DraftResponse:
    draft_path = _draft_path(batch_id)
    if not draft_path.exists():
        return R1DraftResponse(batch_id=batch_id, exists=False)

    with draft_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    segments: list[SplitSegment] = []
    for raw_segment in payload.get("segments", []):
        try:
            segment = SplitSegment(**raw_segment)
        except Exception:
            continue
        if segment.batch_id == batch_id:
            segments.append(with_derived_state(segment))

    return R1DraftResponse(
        batch_id=batch_id,
        exists=True,
        saved_at=payload.get("updated_at"),
        segments=segments,
    )


def export_r1_csv(request: R1ReviewExportRequest) -> dict[str, list[str] | str]:
    updated_at = datetime.now(timezone.utc).isoformat()
    out_dir = REVIEW_OUTPUT_ROOT / "r1" / "exports" / request.batch_id
    out_dir.mkdir(parents=True, exist_ok=True)
    segments = [with_derived_state(segment) for segment in request.segments]
    files = [
        _write_csv(out_dir / "reviewed_render_anchors.csv", RENDER_ANCHOR_FIELDS, reviewed_render_anchor_rows(segments, updated_at)),
        _write_csv(out_dir / "split_marker_review.csv", MARKER_REVIEW_FIELDS, marker_review_rows(segments, updated_at)),
        _write_csv(out_dir / "segment_qc_sheet.csv", SEGMENT_QC_FIELDS, segment_qc_rows(segments, updated_at)),
    ]
    return {"path": str(out_dir), "files": [str(path) for path in files]}


def reviewed_render_anchor_rows(segments: list[SplitSegment], updated_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for segment in segments:
        markers = _marker_map(segment)
        rows.append(
            {
                "batch_id": segment.batch_id,
                "take_id": segment.take_id,
                "segment_id": segment.segment_id,
                "source_audio": segment.relative_path,
                "event_id": segment.event_id,
                "event_range": segment.event_range,
                "variant": segment.variant,
                "pre_idle_end_s": _marker_time(markers.get("pre_idle_end")),
                "gesture_start_s": _marker_time(markers.get("gesture_start")),
                "render_anchor_s": _marker_time(markers.get("render_anchor")),
                "tail_end_s": _marker_time(markers.get("tail_end")),
                "anchor_type": segment.anchor_type,
                "pre_attack_music_policy": segment.pre_attack_music_policy,
                "tail_policy": segment.tail_policy,
                "render_usable": _bool(segment.qc.render_usable),
                "review_status": segment.review_status,
                "review_only": "true",
                "production_grade": "false",
                "not_sample_assets": "true",
                "not_render_executed": "true",
                "updated_at": updated_at,
                "notes": segment.notes,
            }
        )
    return rows


def marker_review_rows(segments: list[SplitSegment], updated_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for segment in segments:
        for marker in _marker_map(segment).values():
            rows.append(
                {
                    "batch_id": segment.batch_id,
                    "take_id": segment.take_id,
                    "segment_id": segment.segment_id,
                    "marker_id": marker.marker_id,
                    "marker_type": marker.marker_type,
                    "marker_label_zh": marker.marker_label_zh,
                    "time_s": f"{marker.time_s:.3f}",
                    "source": marker.source,
                    "confidence": "" if marker.confidence is None else marker.confidence,
                    "review_status": marker.review_status,
                    "nudge_total_ms": marker.nudge_total_ms or 0,
                    "notes": marker.notes,
                    "review_only": "true",
                    "production_grade": "false",
                    "training_value_class": "review_only_render_alignment_draft",
                    "updated_at": updated_at,
                }
            )
    return rows


def segment_qc_rows(segments: list[SplitSegment], updated_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for segment in segments:
        rows.append(
            {
                "batch_id": segment.batch_id,
                "take_id": segment.take_id,
                "segment_id": segment.segment_id,
                "source_audio": segment.relative_path,
                "duration_s": f"{segment.duration_s:.3f}",
                "render_usable": _bool(segment.qc.render_usable),
                "reference_only": _bool(segment.qc.reference_only),
                "unclear": _bool(segment.qc.unclear),
                "needs_retake": _bool(segment.qc.needs_retake),
                "rejected": _bool(segment.qc.rejected),
                "reject_reason": segment.qc.reject_reason,
                "noise_issue": _bool(segment.qc.noise_issue),
                "click_issue": _bool(segment.qc.click_issue),
                "tail_clipped": _bool(segment.qc.tail_clipped),
                "attack_clipped": _bool(segment.qc.attack_clipped),
                "slate_residue": _bool(segment.qc.slate_residue),
                "wrong_take": _bool(segment.qc.wrong_take),
                "notes": segment.notes,
                "review_only": "true",
                "production_grade": "false",
                "not_sample_assets": "true",
                "not_render_executed": "true",
                "updated_at": updated_at,
            }
        )
    return rows


def with_derived_state(segment: SplitSegment) -> SplitSegment:
    markers = _marker_map(segment)
    render_anchor = markers.get("render_anchor")
    tail_end = markers.get("tail_end")
    core = [marker for marker in [render_anchor, tail_end] if marker is not None]
    qc = segment.qc.model_copy()
    review_status = derive_review_status(segment)
    qc.render_usable = derive_render_usable(segment)
    qc.reference_only = segment.segment_status == "reference_only"
    qc.unclear = review_status == "unclear" or segment.segment_status == "unclear"
    qc.needs_retake = any(marker.review_status == "needs_retake" for marker in core) or segment.segment_status == "needs_retake"
    qc.rejected = review_status == "rejected" or segment.segment_status in {"rejected", "excluded"}
    segment_status = segment.segment_status
    if segment_status != "excluded":
        if qc.render_usable:
            segment_status = "render_usable"
        elif qc.reference_only:
            segment_status = "reference_only"
        elif qc.needs_retake:
            segment_status = "needs_retake"
        elif qc.rejected:
            segment_status = "rejected"
        elif qc.unclear:
            segment_status = "unclear"
        else:
            segment_status = "candidate"
    return segment.model_copy(update={"review_status": review_status, "segment_status": segment_status, "qc": qc})


def derive_review_status(segment: SplitSegment) -> str:
    markers = _marker_map(segment)
    render_anchor = markers.get("render_anchor")
    tail_end = markers.get("tail_end")
    core = [marker for marker in [render_anchor, tail_end] if marker is not None]
    all_markers = list(markers.values())

    if segment.segment_status == "excluded":
        return "rejected"
    if any(marker.review_status == "needs_retake" for marker in core):
        return "needs_retake"
    if any(marker.review_status == "rejected" for marker in core):
        return "rejected"
    if render_anchor and tail_end and render_anchor.review_status == "accepted" and tail_end.review_status == "accepted":
        return "accepted"
    if any(marker.review_status == "unclear" for marker in all_markers):
        return "unclear"
    if any(marker.review_status != "candidate" or (marker.nudge_total_ms or 0) != 0 for marker in all_markers):
        return "in_progress"
    return "not_started"


def derive_render_usable(segment: SplitSegment) -> bool:
    markers = _marker_map(segment)
    render_anchor = markers.get("render_anchor")
    tail_end = markers.get("tail_end")
    if segment.segment_status == "excluded":
        return False
    if not render_anchor or not tail_end:
        return False
    if render_anchor.review_status != "accepted" or tail_end.review_status != "accepted":
        return False
    if render_anchor.review_status == "rejected" or tail_end.review_status == "rejected":
        return False
    return not (segment.qc.attack_clipped or segment.qc.tail_clipped or segment.qc.wrong_take)


def _marker_map(segment: SplitSegment) -> dict[str, R1Marker]:
    return {
        key: marker
        for key, marker in segment.markers.model_dump().items()
        if marker is not None
        for marker in [R1Marker(**marker)]
    }


def _marker_time(marker: R1Marker | None) -> str:
    return "" if marker is None else f"{marker.time_s:.3f}"


def _change_log_row(segment: SplitSegment) -> dict[str, object]:
    markers = _marker_map(segment)
    return {
        "segment_id": segment.segment_id,
        "segment_status": segment.segment_status,
        "review_status": segment.review_status,
        "anchor_type": segment.anchor_type,
        "pre_attack_music_policy": segment.pre_attack_music_policy,
        "tail_policy": segment.tail_policy,
        "marker_statuses": {key: marker.review_status for key, marker in markers.items()},
        "marker_nudge_total_ms": {key: marker.nudge_total_ms for key, marker in markers.items()},
    }


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> Path:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _bool(value: bool) -> str:
    return str(bool(value)).lower()


def _draft_path(batch_id: str) -> Path:
    safe_batch_id = batch_id.replace("/", "_").replace("\\", "_")
    return REVIEW_OUTPUT_ROOT / "r1" / "drafts" / f"{safe_batch_id}.split_review.json"
