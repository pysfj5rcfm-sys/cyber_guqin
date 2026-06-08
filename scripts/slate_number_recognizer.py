#!/usr/bin/env python3
"""Reusable slate-number recognition planning helper.

This framework script prepares explicit slate expectations for a recording
session and can optionally materialize dry-run framework artifacts. It does
not create clean segments, sample candidates, sample assets, or production
outputs.
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
    read_take_plan,
    take_no_for_row,
    validate_inputs,
    write_csv,
    write_json,
)


EXPECTED_SLATE_FIELDS = [
    "session_id",
    "batch_id",
    "recording_take_no",
    "script_id",
    "gesture_id",
    "expected_number_3digit",
    "variant_pinyin_yao",
    "variant_pinyin_yi",
    "variant_zh_yao",
    "variant_zh_yi",
    "variant_plain_digits",
    "recognition_status",
    "experimental_only",
    "production_grade",
    "not_standard_sample_library",
    "notes",
]

PINYIN_BY_DIGIT = {
    "0": "ling",
    "1": "yao",
    "2": "er",
    "3": "san",
    "4": "si",
    "5": "wu",
    "6": "liu",
    "7": "qi",
    "8": "ba",
    "9": "jiu",
}

ZH_BY_DIGIT = {
    "0": "零",
    "1": "幺",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--raw-audio-dir", required=True, type=Path)
    parser.add_argument("--take-plan", required=True, type=Path)
    parser.add_argument("--batch-range-map", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--asr-segments",
        type=Path,
        help="Optional precomputed ASR segment CSV/JSONL to use in a later recognition pass.",
    )
    parser.add_argument("--execute", action="store_true", help="Write framework artifacts. Defaults to dry-run.")
    return parser.parse_args()


def pinyin_digits(number: str, one: str) -> str:
    mapping = dict(PINYIN_BY_DIGIT)
    mapping["1"] = one
    return " ".join(mapping[digit] for digit in number)


def zh_digits(number: str, one: str) -> str:
    mapping = dict(ZH_BY_DIGIT)
    mapping["1"] = one
    return "".join(mapping[digit] for digit in number)


def build_expected_rows(session_id: str, take_rows: list[dict[str, str]], batch_ranges) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in take_rows:
        take_no = take_no_for_row(row)
        if not take_no:
            continue
        batch_id = first_value(row, ["batch_id"]) or batch_for_take(take_no, batch_ranges)
        rows.append(
            {
                "session_id": session_id,
                "batch_id": batch_id,
                "recording_take_no": take_no,
                "script_id": first_value(row, ["script_id", "recording_id", "event_id"]),
                "gesture_id": first_value(row, ["gesture_id", "normalized_name"]),
                "expected_number_3digit": take_no,
                "variant_pinyin_yao": pinyin_digits(take_no, "yao"),
                "variant_pinyin_yi": pinyin_digits(take_no, "yi"),
                "variant_zh_yao": zh_digits(take_no, "幺"),
                "variant_zh_yi": zh_digits(take_no, "一"),
                "variant_plain_digits": take_no,
                "recognition_status": "planned_manual_or_asr_review",
                **NON_PRODUCTION_FLAGS,
                "notes": "Framework row only; human review is required before any split output can be trusted.",
            }
        )
    return rows


def build_report(session_id: str, raw_files: list[Path], expected_count: int, execute: bool) -> str:
    lines = [
        framework_report_header(session_id, "Slate Recognition Framework Report"),
        "## Scope",
        "",
        "This helper prepares slate-number expectations for an experimental split workflow.",
        "It is reusable for RS_XWC_002_BAIYA_PILOT or another future session because every input path is explicit.",
        "",
        "## Non-production Guardrails",
        "",
        "- experimental_only=true",
        "- production_grade=false",
        "- no clean segment is created",
        "- no sample candidate is created",
        "- no production ingest is created",
        "",
        "## Input Summary",
        "",
        f"- raw_audio_file_count: {len(raw_files)}",
        f"- expected_slate_row_count: {expected_count}",
        f"- mode: {'execute' if execute else 'dry-run'}",
        "",
        "## Next Required Human Step",
        "",
        "Run ASR or manual slate review, then create a reviewed anchor manifest before unit splitting.",
        "",
    ]
    return "\n".join(lines)


def run(args: argparse.Namespace) -> int:
    validate_inputs(args.session_id, args.raw_audio_dir, args.take_plan, args.batch_range_map)
    take_rows = read_take_plan(args.take_plan)
    batch_ranges = read_batch_ranges(args.batch_range_map)
    raw_files = raw_audio_files(args.raw_audio_dir)
    expected_rows = build_expected_rows(args.session_id, take_rows, batch_ranges)
    payload = {
        "session_id": args.session_id,
        "mode": "execute" if args.execute else "dry-run",
        "raw_audio_dir": str(args.raw_audio_dir),
        "take_plan": str(args.take_plan),
        "batch_range_map": str(args.batch_range_map),
        "raw_audio_file_count": len(raw_files),
        "expected_slate_row_count": len(expected_rows),
        "experimental_only": True,
        "production_grade": False,
        "not_standard_sample_library": True,
    }
    if not args.execute:
        print_dry_run("Dry-run: slate recognition framework inputs validated; no files written.", payload)
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "expected_slate_variants.csv", EXPECTED_SLATE_FIELDS, expected_rows)
    write_json(args.output_dir / "slate_recognition_framework_plan.json", payload)
    (args.output_dir / "slate_recognition_framework_report.md").write_text(
        build_report(args.session_id, raw_files, len(expected_rows), execute=True),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
