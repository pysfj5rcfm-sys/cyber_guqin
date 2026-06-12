from __future__ import annotations

from collections.abc import Iterable


MARKER_REVIEW_STATUS = {"candidate", "accepted", "unclear", "needs_retake", "rejected"}
R1_SEGMENT_STATUS = {"candidate", "render_usable", "reference_only", "unclear", "needs_retake", "rejected", "excluded"}
R1_RENDER_ANCHOR_TYPE = {"main_attack", "gesture_start", "context_first_attach"}

CSV_REQUIRED_FIELDS = {
    "reviewed_slate_anchor_manifest.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "unit_id",
        "source_raw_audio",
        "event_id",
        "event_range",
        "gesture_id",
        "expected_sample_type",
        "slate_start_s",
        "slate_end_s",
        "guqin_start_s",
        "tail_end_s",
        "next_slate_start_s",
        "review_status",
        "review_only",
        "production_grade",
        "not_sample_assets",
        "updated_at",
    ),
    "raw_marker_review.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "marker_id",
        "marker_type",
        "time_s",
        "source",
        "review_status",
        "review_only",
        "production_grade",
        "updated_at",
    ),
    "split_plan_from_raw_markers.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "unit_id",
        "source_raw_audio",
        "event_id",
        "event_range",
        "gesture_id",
        "unit_start_s",
        "unit_end_s",
        "slate_start_s",
        "slate_end_s",
        "next_slate_start_s",
        "suggested_clean_start_s",
        "suggested_clean_end_s",
        "tail_end_s",
        "split_plan_role",
        "source_boundary_policy",
        "requires_human_confirmation",
        "not_executed",
        "not_recording_segments",
        "not_sample_assets",
        "review_only",
        "production_grade",
    ),
    "reviewed_render_anchors.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "take_id",
        "segment_id",
        "source_split_audio",
        "event_id",
        "event_range",
        "gesture_id",
        "realization_variant",
        "pre_idle_end_s",
        "gesture_start_s",
        "render_anchor_s",
        "tail_end_s",
        "render_anchor_type",
        "pre_attack_music_policy",
        "tail_policy",
        "segment_status",
        "review_status",
        "review_only",
        "production_grade",
        "not_sample_assets",
        "not_render_executed",
        "not_ml_training_data",
        "updated_at",
    ),
    "split_marker_review.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "segment_id",
        "marker_id",
        "marker_type",
        "time_s",
        "source",
        "review_status",
        "nudge_total_ms",
        "review_only",
        "production_grade",
        "not_sample_assets",
        "not_render_executed",
        "not_ml_training_data",
        "updated_at",
    ),
    "segment_qc_sheet.csv": (
        "recording_session_id",
        "recording_id",
        "piece_id",
        "qinist_id",
        "batch_id",
        "recording_take_no",
        "batch_take_no",
        "script_id",
        "segment_id",
        "source_split_audio",
        "event_id",
        "event_range",
        "gesture_id",
        "realization_variant",
        "duration_s",
        "segment_status",
        "render_usable",
        "reference_only",
        "unclear",
        "needs_retake",
        "rejected",
        "excluded",
        "human_accepted",
        "reviewed_by",
        "reviewed_at",
        "reject_reason",
        "noise_issue",
        "click_issue",
        "tail_clipped",
        "attack_clipped",
        "slate_residue",
        "wrong_take",
        "review_only",
        "production_grade",
        "not_sample_assets",
        "not_render_executed",
        "not_ml_training_data",
        "updated_at",
    ),
}

PRIMARY_CSVS = {
    "reviewed_slate_anchor_manifest.csv",
    "split_plan_from_raw_markers.csv",
    "reviewed_render_anchors.csv",
    "segment_qc_sheet.csv",
}


def validate_csv_contract(csv_name: str, rows: Iterable[dict[str, object]]) -> list[str]:
    required = CSV_REQUIRED_FIELDS[csv_name]
    warnings: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        missing_columns = [field for field in required if field not in row]
        if missing_columns:
            raise ValueError(f"{csv_name} row {row_index}: missing required columns: {', '.join(missing_columns)}")

        warnings.extend(_warn_empty_required(csv_name, row_index, row, required))
        _validate_status_fields(csv_name, row_index, row)
        _validate_safety_fields(csv_name, row_index, row)
        _validate_aliases(csv_name, row_index, row)
        _validate_no_chinese_contract_values(csv_name, row_index, row)
        _validate_split_plan(csv_name, row_index, row)
    return warnings


def _warn_empty_required(csv_name: str, row_index: int, row: dict[str, object], required: tuple[str, ...]) -> list[str]:
    if csv_name not in PRIMARY_CSVS:
        return []
    warnings = []
    for field in required:
        if field in {"reviewed_at", "reject_reason"}:
            continue
        if row.get(field) in {"", None}:
            warnings.append(f"{csv_name} row {row_index}: required field {field} has no upstream provenance value")
    if csv_name == "segment_qc_sheet.csv" and row.get("reviewed_at") in {"", None}:
        warnings.append(f"{csv_name} row {row_index}: reviewed_at is empty; updated_at was not substituted")
    if csv_name == "segment_qc_sheet.csv" and row.get("segment_status") in {"rejected", "excluded"} and row.get("reject_reason") in {"", None}:
        warnings.append(f"{csv_name} row {row_index}: reject_reason is empty for rejected/excluded segment")
    return warnings


def _validate_status_fields(csv_name: str, row_index: int, row: dict[str, object]) -> None:
    review_status = row.get("review_status")
    if review_status not in {None, ""} and str(review_status) not in MARKER_REVIEW_STATUS:
        raise ValueError(f"{csv_name} row {row_index}: invalid review_status {review_status!r}")
    segment_status = row.get("segment_status")
    if segment_status not in {None, ""} and str(segment_status) not in R1_SEGMENT_STATUS:
        raise ValueError(f"{csv_name} row {row_index}: invalid segment_status {segment_status!r}")
    anchor_type = row.get("render_anchor_type")
    if anchor_type not in {None, ""} and str(anchor_type) not in R1_RENDER_ANCHOR_TYPE:
        raise ValueError(f"{csv_name} row {row_index}: invalid render_anchor_type {anchor_type!r}")


def _validate_safety_fields(csv_name: str, row_index: int, row: dict[str, object]) -> None:
    expected = {
        "review_only": "true",
        "production_grade": "false",
        "not_sample_assets": "true",
    }
    if csv_name == "split_plan_from_raw_markers.csv":
        expected.update({"not_executed": "true", "not_recording_segments": "true"})
    if csv_name in {"reviewed_render_anchors.csv", "split_marker_review.csv", "segment_qc_sheet.csv"}:
        expected.update({"not_render_executed": "true", "not_ml_training_data": "true"})
    for field, value in expected.items():
        if str(row.get(field)).lower() != value:
            raise ValueError(f"{csv_name} row {row_index}: expected {field}={value}")


def _validate_aliases(csv_name: str, row_index: int, row: dict[str, object]) -> None:
    pairs = [
        ("realization_variant", "variant"),
        ("render_anchor_type", "anchor_type"),
    ]
    if csv_name in {"reviewed_slate_anchor_manifest.csv", "raw_marker_review.csv", "split_plan_from_raw_markers.csv"}:
        pairs.append(("source_raw_audio", "source_audio"))
    if csv_name in {"reviewed_render_anchors.csv", "split_marker_review.csv", "segment_qc_sheet.csv"}:
        pairs.append(("source_split_audio", "source_audio"))
    for canonical, alias in pairs:
        if canonical in row and alias in row and row.get(canonical) not in {"", None} and row.get(alias) not in {"", None}:
            if row.get(canonical) != row.get(alias):
                raise ValueError(f"{csv_name} row {row_index}: alias {alias} conflicts with {canonical}")


def _validate_no_chinese_contract_values(csv_name: str, row_index: int, row: dict[str, object]) -> None:
    contract_value_fields = {"review_status", "segment_status", "unit_status", "render_anchor_type", "anchor_type"}
    for field, value in row.items():
        if field not in contract_value_fields or field.endswith("_label_zh") or value in {None, ""}:
            continue
        if any("\u4e00" <= char <= "\u9fff" for char in str(value)):
            raise ValueError(f"{csv_name} row {row_index}: Chinese text is only allowed in *_label_zh fields")


def _validate_split_plan(csv_name: str, row_index: int, row: dict[str, object]) -> None:
    if csv_name != "split_plan_from_raw_markers.csv":
        return
    if row.get("split_plan_role") not in {"unit_preview", "clean_preview"}:
        raise ValueError(f"{csv_name} row {row_index}: invalid split_plan_role {row.get('split_plan_role')!r}")
