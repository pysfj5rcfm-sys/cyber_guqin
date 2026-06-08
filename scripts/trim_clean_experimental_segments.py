#!/usr/bin/env python3
"""Reusable unit-internal slate trim planning helper.

This framework script prepares clean-segment trim metadata only after reviewed
unit previews exist. It defaults to dry-run and labels every artifact as
experimental-only and non-production.
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


CLEAN_PLAN_FIELDS = [
    "session_id",
    "clean_segment_id",
    "batch_id",
    "recording_take_no",
    "script_id",
    "gesture_id",
    "source_unit_preview_file_path",
    "trim_start_time_s",
    "trim_end_time_s",
    "clean_segment_status",
    "contains_leading_slate",
    "possible_next_slate_residue",
    "needs_manual_review",
    "qc_status",
    "selected_for_sample_candidate",
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
        "--reviewed-unit-preview-manifest",
        type=Path,
        help="Optional reviewed unit preview CSV. Without it, trim rows remain blocked.",
    )
    parser.add_argument("--execute", action="store_true", help="Write framework artifacts. Defaults to dry-run.")
    return parser.parse_args()


def unit_lookup(path: Path | None) -> dict[str, dict[str, str]]:
    if not path:
        return {}
    rows = read_csv_rows(path)
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        take_no = take_no_for_row(row)
        if take_no:
            lookup[take_no] = row
    return lookup


def build_clean_rows(
    session_id: str,
    take_rows: list[dict[str, str]],
    batch_ranges,
    units: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for take_row in take_rows:
        take_no = take_no_for_row(take_row)
        if not take_no:
            continue
        unit = units.get(take_no, {})
        has_reviewed_unit = bool(unit and first_value(unit, ["unit_status", "review_decision"]))
        clean_id = f"{session_id}_EXP_CLEAN_{take_no}"
        rows.append(
            {
                "session_id": session_id,
                "clean_segment_id": clean_id,
                "batch_id": first_value(take_row, ["batch_id"]) or batch_for_take(take_no, batch_ranges),
                "recording_take_no": take_no,
                "script_id": first_value(take_row, ["script_id", "recording_id", "event_id"]),
                "gesture_id": first_value(take_row, ["gesture_id", "normalized_name"]),
                "source_unit_preview_file_path": first_value(unit, ["unit_preview_file_path", "source_unit_preview_file_path"]),
                "trim_start_time_s": "",
                "trim_end_time_s": first_value(unit, ["unit_end_time_s"]),
                "clean_segment_status": "planned_needs_human_qc" if has_reviewed_unit else "blocked_missing_reviewed_unit",
                "contains_leading_slate": "unknown_until_listening_qc",
                "possible_next_slate_residue": "unknown_until_listening_qc",
                "needs_manual_review": "true",
                "qc_status": "not_reviewed",
                "selected_for_sample_candidate": "false",
                **NON_PRODUCTION_FLAGS,
                "notes": "No sample promotion is allowed until human listening QC accepts the clean segment.",
            }
        )
    return rows


def build_report(session_id: str, raw_count: int, clean_count: int, unit_count: int, execute: bool) -> str:
    lines = [
        framework_report_header(session_id, "Clean Experimental Trim Framework Report"),
        "## Scope",
        "",
        "This helper documents the unit-internal slate trim gate for future experimental sessions.",
        "It is not a production sample ingest script.",
        "",
        "## Input Summary",
        "",
        f"- raw_audio_file_count: {raw_count}",
        f"- reviewed_unit_preview_count: {unit_count}",
        f"- planned_clean_row_count: {clean_count}",
        f"- mode: {'execute' if execute else 'dry-run'}",
        "",
        "## Promotion Rule",
        "",
        "A clean segment becomes a sample candidate only after explicit human listening acceptance in a later authorized step.",
        "",
    ]
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    validate_inputs(args.session_id, args.raw_audio_dir, args.take_plan, args.batch_range_map)
    if args.reviewed_unit_preview_manifest and not args.reviewed_unit_preview_manifest.is_file():
        raise SystemExit(f"Missing reviewed unit preview manifest: {args.reviewed_unit_preview_manifest}")
    take_rows = read_take_plan(args.take_plan)
    batch_ranges = read_batch_ranges(args.batch_range_map)
    units = unit_lookup(args.reviewed_unit_preview_manifest)
    raw_count = len(raw_audio_files(args.raw_audio_dir))
    clean_rows = build_clean_rows(args.session_id, take_rows, batch_ranges, units)
    payload = {
        "session_id": args.session_id,
        "mode": "execute" if args.execute else "dry-run",
        "raw_audio_dir": str(args.raw_audio_dir),
        "take_plan": str(args.take_plan),
        "batch_range_map": str(args.batch_range_map),
        "reviewed_unit_preview_manifest": str(args.reviewed_unit_preview_manifest or ""),
        "planned_clean_row_count": len(clean_rows),
        "reviewed_unit_preview_count": len(units),
        "experimental_only": True,
        "production_grade": False,
        "not_standard_sample_library": True,
        "sample_candidate_created": False,
    }
    if not args.execute:
        print_dry_run("Dry-run: clean trim framework inputs validated; no files written.", payload)
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "clean_experimental_trim_framework_manifest.csv", CLEAN_PLAN_FIELDS, clean_rows)
    write_json(args.output_dir / "clean_experimental_trim_framework_plan.json", payload)
    (args.output_dir / "clean_experimental_trim_framework_report.md").write_text(
        build_report(args.session_id, raw_count, len(clean_rows), len(units), execute=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
