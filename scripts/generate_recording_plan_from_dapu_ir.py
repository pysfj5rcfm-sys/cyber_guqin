#!/usr/bin/env python3
"""Generate a manifest-driven recording plan from Dapu Event IR.

The tool is dry-run-first. It never creates raw-audio folders, sample ingest
files, review data, or render outputs.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Any

from cyber_guqin_reproduction_lib import (
    ToolError,
    fail,
    load_json_compatible_yaml,
    load_jsonl,
    print_payload,
    require_fields,
    sha256_file,
    write_csv,
    write_json,
)


REQUIRED_EVENT_FIELDS = [
    "event_id",
    "phrase_id",
    "score_order",
    "sound_type",
    "string",
    "hui_position",
    "technique",
    "gesture_family",
    "special_technique",
    "needs_context_take",
    "needs_long_tail",
    "needs_retake",
    "source_confidence",
    "needs_review",
]

TAKE_FIELDS = [
    "piece_id",
    "session_id",
    "recording_id",
    "qinist_id",
    "qinist_name",
    "recording_take_no",
    "batch_id",
    "batch_take_no",
    "event_id",
    "phrase_id",
    "score_order",
    "sound_type",
    "string",
    "hui_position",
    "technique",
    "gesture_family",
    "special_technique",
    "is_context_take",
    "needs_retake",
    "source_confidence",
    "needs_review",
    "tail_policy",
    "slate_text",
    "spoken_slate_text",
    "human_review_status",
    "notes",
]

BATCH_FIELDS = [
    "batch_id",
    "start_recording_take_no",
    "end_recording_take_no",
    "expected_take_count",
    "recording_mode",
    "notes",
]

GAP_FIELDS = [
    "event_id",
    "phrase_id",
    "gap_type",
    "severity",
    "reason",
    "human_action",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--piece-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--recording-id", required=True)
    parser.add_argument("--qinist-id", required=True)
    parser.add_argument("--qinist-name", required=True)
    parser.add_argument("--dapu-ir", required=True, type=Path)
    parser.add_argument("--recording-config", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the planned outputs without writing files.")
    parser.add_argument("--execute", action="store_true", help="Write recording-plan artifacts. Defaults to dry-run.")
    return parser.parse_args()


def validate_events(events: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    seen: set[str] = set()
    for index, event in enumerate(events, start=1):
        event_id = str(event.get("event_id") or f"row_{index}")
        missing = [field for field in REQUIRED_EVENT_FIELDS if field not in event]
        if missing:
            errors.append(f"{event_id}: missing required field(s): {', '.join(missing)}")
        if event_id in seen:
            errors.append(f"{event_id}: duplicate event_id")
        seen.add(event_id)
    if errors:
        raise ToolError("invalid Dapu IR:\n- " + "\n- ".join(errors))


def z3(value: int) -> str:
    return f"{value:03d}"


def slate_text(take_no: str, event: dict[str, Any], config: dict[str, Any]) -> str:
    template = (
        config.get("slate_policy", {}).get("template")
        if isinstance(config.get("slate_policy"), dict)
        else None
    ) or "slate {take_no} {event_id} {technique}"
    return str(template).format(
        take_no=take_no,
        event_id=event.get("event_id", ""),
        phrase_id=event.get("phrase_id", ""),
        technique=event.get("technique", ""),
    )


def tail_policy(event: dict[str, Any], config: dict[str, Any]) -> str:
    policy = config.get("tail_policy") if isinstance(config.get("tail_policy"), dict) else {}
    if event.get("needs_long_tail") is True:
        return str(policy.get("long_tail") or "full_tail")
    return str(policy.get("default") or "full_tail")


def build_take_rows(args: argparse.Namespace, events: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    max_batch_size = int(config.get("max_batch_size") or 10)
    rows: list[dict[str, Any]] = []
    for index, event in enumerate(sorted(events, key=lambda item: int(item.get("score_order", 0))), start=1):
        take_no = z3(index)
        batch_index = math.ceil(index / max_batch_size)
        batch_start = (batch_index - 1) * max_batch_size
        is_context = bool(event.get("needs_context_take"))
        notes = ["draft_pending_human_review"]
        if is_context:
            notes.append("context_take_policy=manifest_driven")
        if event.get("needs_long_tail"):
            notes.append("long_tail_policy=manifest_driven")
        if event.get("needs_retake"):
            notes.append("needs_retake=true")
        rows.append(
            {
                "piece_id": args.piece_id,
                "session_id": args.session_id,
                "recording_id": args.recording_id,
                "qinist_id": args.qinist_id,
                "qinist_name": args.qinist_name,
                "recording_take_no": take_no,
                "batch_id": f"batch{batch_index:02d}",
                "batch_take_no": z3(index - batch_start),
                "event_id": event.get("event_id", ""),
                "phrase_id": event.get("phrase_id", ""),
                "score_order": event.get("score_order", ""),
                "sound_type": event.get("sound_type", ""),
                "string": event.get("string", ""),
                "hui_position": event.get("hui_position", ""),
                "technique": event.get("technique", ""),
                "gesture_family": event.get("gesture_family", ""),
                "special_technique": event.get("special_technique", ""),
                "is_context_take": "true" if is_context else "false",
                "needs_retake": "true" if event.get("needs_retake") else "false",
                "source_confidence": event.get("source_confidence", ""),
                "needs_review": "true" if event.get("needs_review") else "false",
                "tail_policy": tail_policy(event, config),
                "slate_text": slate_text(take_no, event, config),
                "spoken_slate_text": slate_text(take_no, event, config),
                "human_review_status": "required" if event.get("needs_review") else "ready_for_review",
                "notes": "; ".join(notes),
            }
        )
    return rows


def build_batch_rows(take_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_batch: dict[str, list[dict[str, Any]]] = {}
    for row in take_rows:
        by_batch.setdefault(str(row["batch_id"]), []).append(row)
    for batch_id, items in sorted(by_batch.items()):
        rows.append(
            {
                "batch_id": batch_id,
                "start_recording_take_no": items[0]["recording_take_no"],
                "end_recording_take_no": items[-1]["recording_take_no"],
                "expected_take_count": len(items),
                "recording_mode": "draft_recording_plan",
                "notes": "human approval required before recording",
            }
        )
    return rows


def build_gap_rows(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for event in events:
        event_id = str(event.get("event_id", ""))
        confidence = float(event.get("source_confidence") or 0)
        if event.get("needs_review") is True:
            rows.append(
                {
                    "event_id": event_id,
                    "phrase_id": str(event.get("phrase_id", "")),
                    "gap_type": "human_review_required",
                    "severity": "medium",
                    "reason": "Dapu IR row has needs_review=true",
                    "human_action": "confirm score facts and qinist realization before recording",
                }
            )
        if confidence < 0.75:
            rows.append(
                {
                    "event_id": event_id,
                    "phrase_id": str(event.get("phrase_id", "")),
                    "gap_type": "low_source_confidence",
                    "severity": "medium",
                    "reason": f"source_confidence={confidence}",
                    "human_action": "review source evidence before treating this as a stable recording item",
                }
            )
    return rows


def expected_paths(output_root: Path) -> dict[str, str]:
    return {
        "recording_take_plan.csv": str(output_root / "recording_take_plan.csv"),
        "recording_batch_plan.csv": str(output_root / "recording_batch_plan.csv"),
        "recording_coverage_gap.csv": str(output_root / "recording_coverage_gap.csv"),
        "recording_plan_human_review.md": str(output_root / "recording_plan_human_review.md"),
        "recording_plan_manifest.json": str(output_root / "recording_plan_manifest.json"),
    }


def build_human_review(args: argparse.Namespace, summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Recording Plan Human Review",
            "",
            f"- piece_id: `{args.piece_id}`",
            f"- session_id: `{args.session_id}`",
            f"- recording_id: `{args.recording_id}`",
            f"- qinist_id: `{args.qinist_id}`",
            f"- qinist_name: `{args.qinist_name}`",
            f"- take_count: `{summary['take_count']}`",
            f"- batch_count: `{summary['batch_count']}`",
            f"- coverage_gap_count: `{summary['coverage_gap_count']}`",
            "",
            "Human approval is required before recording, R0 review, render, sample ingest, or ML work.",
            "",
        ]
    )


def run(args: argparse.Namespace) -> int:
    config = load_json_compatible_yaml(args.recording_config)
    require_fields(config, ["max_batch_size", "tail_policy", "context_take_policy", "output_settings"], "recording config")
    events = load_jsonl(args.dapu_ir)
    validate_events(events)

    take_rows = build_take_rows(args, events, config)
    batch_rows = build_batch_rows(take_rows)
    gap_rows = build_gap_rows(events)
    summary = {
        "piece_id": args.piece_id,
        "session_id": args.session_id,
        "recording_id": args.recording_id,
        "qinist_id": args.qinist_id,
        "mode": "execute" if args.execute else "dry-run",
        "take_count": len(take_rows),
        "batch_count": len(batch_rows),
        "coverage_gap_count": len(gap_rows),
        "expected_output_paths": expected_paths(args.output_root),
        "warnings": [
            "recording plan is not sample ingest",
            "human approval is required before recording or review execution",
        ],
    }

    if not args.execute:
        print_payload({"status": "DRY_RUN", **summary})
        return 0

    args.output_root.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_root / "recording_take_plan.csv", TAKE_FIELDS, take_rows)
    write_csv(args.output_root / "recording_batch_plan.csv", BATCH_FIELDS, batch_rows)
    write_csv(args.output_root / "recording_coverage_gap.csv", GAP_FIELDS, gap_rows)
    (args.output_root / "recording_plan_human_review.md").write_text(
        build_human_review(args, summary),
        encoding="utf-8",
    )
    manifest = {
        "manifest_schema": "cyber_guqin.recording_plan.v0.1",
        "dry_run_default": True,
        "dapu_ir": str(args.dapu_ir),
        "dapu_ir_sha256": sha256_file(args.dapu_ir),
        "recording_config": str(args.recording_config),
        "recording_config_sha256": sha256_file(args.recording_config),
        "row_counts": {
            "recording_take_plan.csv": len(take_rows),
            "recording_batch_plan.csv": len(batch_rows),
            "recording_coverage_gap.csv": len(gap_rows),
        },
        **summary,
    }
    write_json(args.output_root / "recording_plan_manifest.json", manifest)
    print_payload({"status": "EXECUTE_WRITTEN", **summary})
    return 0


def main() -> int:
    try:
        return run(parse_args())
    except ToolError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
