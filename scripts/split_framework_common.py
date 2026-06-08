#!/usr/bin/env python3
"""Shared helpers for reusable experimental recording split scripts."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


NON_PRODUCTION_FLAGS = {
    "experimental_only": "true",
    "production_grade": "false",
    "not_standard_sample_library": "true",
}


@dataclass(frozen=True)
class BatchRange:
    batch_id: str
    start_take: str
    end_take: str

    def contains(self, take_no: str) -> bool:
        return int(self.start_take) <= int(take_no) <= int(self.end_take)


def z3(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return f"{int(text):03d}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_take_plan(path: Path) -> list[dict[str, str]]:
    if path.suffix.lower() == ".csv":
        return read_csv_rows(path)
    if path.suffix.lower() == ".jsonl":
        rows: list[dict[str, str]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            for key in ["items", "takes", "recording_items", "rows"]:
                value = payload.get(key)
                if isinstance(value, list):
                    return value
        raise SystemExit(f"Unsupported take-plan JSON shape: {path}")
    raise SystemExit(f"Unsupported take-plan format, expected csv/json/jsonl: {path}")


def read_batch_ranges(path: Path) -> list[BatchRange]:
    rows = read_csv_rows(path)
    ranges: list[BatchRange] = []
    for row in rows:
        batch_id = first_value(row, ["batch_id", "batch", "source_batch_id"])
        start_take = first_value(
            row,
            [
                "start_recording_take_no",
                "start_take",
                "start_take_no",
                "recording_take_no_start",
                "first_take",
            ],
        )
        end_take = first_value(
            row,
            [
                "end_recording_take_no",
                "end_take",
                "end_take_no",
                "recording_take_no_end",
                "last_take",
            ],
        )
        if not (batch_id and start_take and end_take):
            raise SystemExit(f"Batch range row is missing batch/start/end fields: {row}")
        ranges.append(BatchRange(batch_id=batch_id, start_take=z3(start_take), end_take=z3(end_take)))
    return ranges


def first_value(row: dict[str, object], names: list[str]) -> str:
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def take_no_for_row(row: dict[str, object]) -> str:
    return z3(first_value(row, ["recording_take_no", "take_no", "slate_number", "expected_number_3digit"]))


def batch_for_take(take_no: str, ranges: list[BatchRange]) -> str:
    if not take_no:
        return ""
    for batch_range in ranges:
        if batch_range.contains(take_no):
            return batch_range.batch_id
    return ""


def raw_audio_files(raw_audio_dir: Path) -> list[Path]:
    suffixes = {".wav", ".m4a", ".aif", ".aiff", ".flac"}
    return sorted(path for path in raw_audio_dir.iterdir() if path.is_file() and path.suffix.lower() in suffixes)


def validate_inputs(session_id: str, raw_audio_dir: Path, take_plan: Path, batch_range_map: Path) -> None:
    if not session_id.strip():
        raise SystemExit("--session-id must not be empty")
    if not raw_audio_dir.is_dir():
        raise SystemExit(f"Missing raw audio dir: {raw_audio_dir}")
    if not take_plan.is_file():
        raise SystemExit(f"Missing take plan: {take_plan}")
    if not batch_range_map.is_file():
        raise SystemExit(f"Missing batch range map: {batch_range_map}")


def framework_report_header(session_id: str, title: str) -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            f"- session_id: {session_id}",
            "- asset_class: mvp_experimental_raw",
            "- experimental_only: true",
            "- production_grade: false",
            "- not_standard_sample_library: true",
            "- sample_candidate_created: false",
            "- production_ingest_created: false",
            "",
        ]
    )


def print_dry_run(message: str, payload: dict[str, object]) -> None:
    print(message)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
