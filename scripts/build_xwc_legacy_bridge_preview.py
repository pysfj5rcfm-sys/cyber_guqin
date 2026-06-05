#!/usr/bin/env python3
"""Build a read-only XWC legacy recording bridge preview.

This script reads the legacy Phase 1A recording scripts and writes preview
artifacts under reports/. It does not create ingest data, real manifests,
recording segments, sample assets, or audio files.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDING_SCRIPT = ROOT / "01_pieces/xianwengcao/recording_script.csv"
HUMAN_SCRIPT = ROOT / "01_pieces/xianwengcao/recording_script_human.csv"
SCORE_EVENTS = ROOT / "01_pieces/xianwengcao/score_events.csv"
REPORTS = ROOT / "reports"
MAP_OUT = REPORTS / "xwc_legacy_recording_bridge_map.json"
CSV_OUT = REPORTS / "xwc_legacy_take_manifest_preview.csv"

TAKE_MANIFEST_FIELDS = [
    "recording_session_id",
    "recording_id",
    "recording_take_no",
    "batch_take_no",
    "script_id",
    "legacy_source_type",
    "legacy_source_path",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "realization_pre_action",
    "source_raw_file",
    "take_start_time_s",
    "take_end_time_s",
    "slate_text",
    "take_quality",
    "performer_note",
    "engineer_note",
    "needs_reshoot",
    "selected_for_segment",
    "selected_for_sample",
    "notes",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build() -> None:
    script_rows = read_csv(RECORDING_SCRIPT)
    human_rows = read_csv(HUMAN_SCRIPT)
    score_event_ids = {row["event_id"] for row in read_csv(SCORE_EVENTS)}
    human_by_script_id = {row["script_id"]: row for row in human_rows}

    sample_type_counts = Counter(row["expected_sample_type"] for row in script_rows)
    variant_counts = Counter(row["realization_variant"] for row in script_rows)
    context_missing_event_range = [
        row
        for row in script_rows
        if row["expected_sample_type"] == "context" and not row["event_range"]
    ]

    items: list[dict[str, object]] = []
    preview_rows: list[dict[str, str]] = []
    top_warnings: list[str] = []

    if len(script_rows) != 71:
        top_warnings.append(f"Expected 71 recording tasks, found {len(script_rows)}.")
    if len(human_rows) != len(script_rows):
        top_warnings.append(
            f"Human script row count {len(human_rows)} differs from recording_script row count {len(script_rows)}."
        )

    for row in script_rows:
        human = human_by_script_id.get(row["script_id"], {})
        item_warnings: list[str] = []

        if not human:
            item_warnings.append("No matching recording_script_human.csv row.")
        if row["event_id"] and row["event_id"] not in score_event_ids:
            item_warnings.append("event_id not found in score_events.csv.")
        if row["expected_sample_type"] == "context" and not row["event_range"]:
            item_warnings.append(
                "Context take is missing event_range; resolve before slicing or segment registration."
            )

        recording_take_no = human.get("recording_take_no") or row.get("order_no", "")
        batch_take_no = human.get("batch_take_no", "")
        notes = row.get("notes", "")
        if item_warnings:
            notes = (notes + " | " if notes else "") + "WARNING: " + "; ".join(item_warnings)

        item = {
            "recording_take_no": recording_take_no,
            "batch_take_no": batch_take_no,
            "script_id": row["script_id"],
            "event_id": row["event_id"] or None,
            "event_range": row["event_range"] or None,
            "gesture_id": row["gesture_id"] or None,
            "normalized_name": row["normalized_name"] or None,
            "expected_sample_type": row["expected_sample_type"] or None,
            "realization_variant": row["realization_variant"] or None,
            "realization_pre_action": row["realization_pre_action"] or None,
            "auto_fill_status": "needs_user_review" if item_warnings else "auto_filled_from_legacy_script",
            "needs_user_review": bool(item_warnings),
            "warnings": item_warnings,
        }
        items.append(item)

        preview_rows.append(
            {
                "recording_session_id": "",
                "recording_id": row["recording_id"],
                "recording_take_no": recording_take_no,
                "batch_take_no": batch_take_no,
                "script_id": row["script_id"],
                "legacy_source_type": "legacy_v1_recording_script",
                "legacy_source_path": rel(RECORDING_SCRIPT),
                "event_id": row["event_id"],
                "event_range": row["event_range"],
                "gesture_id": row["gesture_id"],
                "normalized_name": row["normalized_name"],
                "expected_sample_type": row["expected_sample_type"],
                "realization_variant": row["realization_variant"],
                "realization_pre_action": row["realization_pre_action"],
                "source_raw_file": "",
                "take_start_time_s": "",
                "take_end_time_s": "",
                "slate_text": batch_take_no or recording_take_no,
                "take_quality": "",
                "performer_note": "",
                "engineer_note": "",
                "needs_reshoot": "",
                "selected_for_segment": "",
                "selected_for_sample": "",
                "notes": notes,
            }
        )

    if context_missing_event_range:
        top_warnings.append(
            "Context event_range missing for "
            + ", ".join(
                f"{row['script_id']} (order_no {row['order_no']}, event_id {row['event_id']})"
                for row in context_missing_event_range
            )
            + "."
        )

    bridge_map = {
        "bridge_type": "xwc_legacy_recording_script_to_reusable_recording_asset_model",
        "piece_id": "XWC",
        "recording_id": "RS_XWC_001",
        "is_legacy_bridge": True,
        "do_not_treat_as_ingest_data": True,
        "source_files": {
            "recording_script": rel(RECORDING_SCRIPT),
            "recording_script_human": rel(HUMAN_SCRIPT),
            "score_events": rel(SCORE_EVENTS),
        },
        "summary": {
            "total_tasks": len(script_rows),
            "atomic_count": sample_type_counts.get("atomic", 0),
            "context_count": sample_type_counts.get("context", 0),
            "straight_count": variant_counts.get("straight", 0),
            "chuo_count": variant_counts.get("chuo", 0),
            "zhu_count": variant_counts.get("zhu", 0),
            "missing_event_range_count": len(context_missing_event_range),
            "context_missing_event_range_count": len(context_missing_event_range),
            "all_blank_event_range_count": sum(1 for row in script_rows if not row["event_range"]),
        },
        "items": items,
        "warnings": top_warnings,
        "future_policy": {
            "recording_batches_md_is_execution_view_only": True,
            "future_source_should_be_dapu_event_ir": True,
        },
    }

    REPORTS.mkdir(exist_ok=True)
    with MAP_OUT.open("w", encoding="utf-8") as handle:
        json.dump(bridge_map, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    with CSV_OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=TAKE_MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(preview_rows)

    print(f"Wrote {rel(MAP_OUT)} with {len(items)} preview items.")
    print(f"Wrote {rel(CSV_OUT)} with {len(preview_rows)} preview rows.")
    if top_warnings:
        print("Warnings:")
        for warning in top_warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    build()
