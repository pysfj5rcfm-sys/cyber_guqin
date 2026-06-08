#!/usr/bin/env python3
"""Reusable reviewed-anchor finalization helper.

This framework script records the handoff from reviewed slate anchors to
anchor-locked unit preview planning. It never promotes audio to sample
candidate status and never writes production ingest data.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from split_framework_common import (
    NON_PRODUCTION_FLAGS,
    batch_for_take,
    first_value,
    framework_report_header,
    print_dry_run,
    raw_audio_files,
    read_batch_ranges,
    read_csv_rows,
    read_take_plan,
    take_no_for_row,
    validate_inputs,
    write_csv,
    write_json,
)


FINAL_UNIT_FIELDS = [
    "session_id",
    "batch_id",
    "recording_take_no",
    "script_id",
    "gesture_id",
    "expected_number_3digit",
    "anchor_start_time_s",
    "anchor_end_time_s",
    "next_anchor_start_time_s",
    "unit_start_time_s",
    "unit_end_time_s",
    "unit_status",
    "needs_manual_review",
    "review_reason",
    "experimental_only",
    "production_grade",
    "not_standard_sample_library",
    "notes",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--raw-audio-dir", required=True, type=Path)
    parser.add_argument("--take-plan", required=True, type=Path)
    parser.add_argument("--batch-range-map", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--reviewed-anchor-manifest",
        type=Path,
        help="Optional reviewed anchor CSV. Without it, output rows remain blocked for review.",
    )
    parser.add_argument("--execute", action="store_true", help="Write framework artifacts. Defaults to dry-run.")
    return parser.parse_args()


def anchor_lookup(path: Path | None) -> dict[str, dict[str, str]]:
    if not path:
        return {}
    rows = read_csv_rows(path)
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        take_no = take_no_for_row(row)
        if take_no:
            lookup[take_no] = row
    return lookup


def build_unit_rows(
    session_id: str,
    take_rows: list[dict[str, str]],
    batch_ranges,
    anchors: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index, take_row in enumerate(take_rows):
        take_no = take_no_for_row(take_row)
        if not take_no:
            continue
        next_take_no = ""
        for later_row in take_rows[index + 1 :]:
            next_take_no = take_no_for_row(later_row)
            if next_take_no:
                break
        anchor = anchors.get(take_no, {})
        next_anchor = anchors.get(next_take_no, {})
        has_reviewed_boundaries = bool(anchor and first_value(anchor, ["anchor_start_time_s", "reviewed_anchor_start_time_s"]))
        rows.append(
            {
                "session_id": session_id,
                "batch_id": first_value(take_row, ["batch_id"]) or batch_for_take(take_no, batch_ranges),
                "recording_take_no": take_no,
                "script_id": first_value(take_row, ["script_id", "recording_id", "event_id"]),
                "gesture_id": first_value(take_row, ["gesture_id", "normalized_name"]),
                "expected_number_3digit": take_no,
                "anchor_start_time_s": first_value(anchor, ["reviewed_anchor_start_time_s", "anchor_start_time_s"]),
                "anchor_end_time_s": first_value(anchor, ["reviewed_anchor_end_time_s", "anchor_end_time_s"]),
                "next_anchor_start_time_s": first_value(
                    next_anchor, ["reviewed_anchor_start_time_s", "anchor_start_time_s"]
                ),
                "unit_start_time_s": first_value(anchor, ["reviewed_anchor_start_time_s", "anchor_start_time_s"]),
                "unit_end_time_s": "",
                "unit_status": "planned_anchor_locked_preview" if has_reviewed_boundaries else "blocked_missing_reviewed_anchor",
                "needs_manual_review": "true",
                "review_reason": "human reviewed anchor manifest required before preview audio can be trusted",
                **NON_PRODUCTION_FLAGS,
                "notes": "Framework row only; reviewed unit previews still require listening QC.",
            }
        )
    return rows


def build_report(session_id: str, raw_count: int, unit_count: int, anchor_count: int, execute: bool) -> str:
    lines = [
        framework_report_header(session_id, "Reviewed Unit Preview Finalization Framework Report"),
        "## Scope",
        "",
        "This helper preserves the batch range lock -> reviewed anchors -> anchor-locked unit preview handoff.",
        "It does not cut audio by default and it does not create clean segments.",
        "",
        "## Input Summary",
        "",
        f"- raw_audio_file_count: {raw_count}",
        f"- reviewed_anchor_count: {anchor_count}",
        f"- planned_unit_row_count: {unit_count}",
        f"- mode: {'execute' if execute else 'dry-run'}",
        "",
        "## Required Next Gate",
        "",
        "Unit previews must be human reviewed before any unit-internal slate trim is attempted.",
        "",
    ]
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    validate_inputs(args.session_id, args.raw_audio_dir, args.take_plan, args.batch_range_map)
    if args.reviewed_anchor_manifest and not args.reviewed_anchor_manifest.is_file():
        raise SystemExit(f"Missing reviewed anchor manifest: {args.reviewed_anchor_manifest}")
    take_rows = read_take_plan(args.take_plan)
    batch_ranges = read_batch_ranges(args.batch_range_map)
    anchors = anchor_lookup(args.reviewed_anchor_manifest)
    raw_count = len(raw_audio_files(args.raw_audio_dir))
    unit_rows = build_unit_rows(args.session_id, take_rows, batch_ranges, anchors)
    payload = {
        "session_id": args.session_id,
        "mode": "execute" if args.execute else "dry-run",
        "raw_audio_dir": str(args.raw_audio_dir),
        "take_plan": str(args.take_plan),
        "batch_range_map": str(args.batch_range_map),
        "reviewed_anchor_manifest": str(args.reviewed_anchor_manifest or ""),
        "planned_unit_row_count": len(unit_rows),
        "reviewed_anchor_count": len(anchors),
        "experimental_only": True,
        "production_grade": False,
        "not_standard_sample_library": True,
    }
    if not args.execute:
        print_dry_run("Dry-run: reviewed unit preview framework inputs validated; no files written.", payload)
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "reviewed_anchor_locked_unit_preview_framework.csv", FINAL_UNIT_FIELDS, unit_rows)
    write_json(args.output_dir / "reviewed_unit_preview_framework_plan.json", payload)
    (args.output_dir / "reviewed_unit_preview_framework_report.md").write_text(
        build_report(args.session_id, raw_count, len(unit_rows), len(anchors), execute=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
