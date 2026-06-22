#!/usr/bin/env python3
"""Shared helpers for dry-run-first Cyber Guqin reproduction tools."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DERIVED_AUTHORITY_NAMES = {
    "issue_list.csv",
    "listening_review.csv",
    "listening_review.yaml",
    "preferred_version_summary.csv",
    "phrase_structure_review.yaml",
    "render_phrase_alignment.csv",
    "phrase_boundary_decision.csv",
    "render_revision_log.yaml",
}
FORBIDDEN_AUTHORITY_MARKERS = (
    "Downloads",
    "browser Blob",
    "browser_Blob",
    "Blob",
    "restore zip",
    "restore_zip",
    ".zip",
)


class ToolError(RuntimeError):
    """Raised for expected validation failures with user-facing messages."""


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def load_json_compatible_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ToolError(f"missing manifest/config file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ToolError(
            f"{path} is not JSON-compatible YAML. These tools intentionally avoid third-party YAML dependencies."
        ) from exc
    if not isinstance(data, dict):
        raise ToolError(f"manifest/config root must be an object: {path}")
    return data


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ToolError(f"missing JSON file: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid JSON file: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ToolError(f"JSON root must be an object: {path}")
    return data


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise ToolError(f"missing JSONL file: {path}")
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ToolError(f"{path}:{line_no} invalid JSONL row: {exc}") from exc
        if not isinstance(item, dict):
            raise ToolError(f"{path}:{line_no} row must be an object")
        rows.append(item)
    if not rows:
        raise ToolError(f"JSONL has no rows: {path}")
    return rows


def require_fields(data: dict[str, Any], fields: list[str], label: str = "manifest") -> None:
    missing = [field for field in fields if field not in data or data.get(field) in (None, "", [])]
    if missing:
        raise ToolError(f"missing required {label} field(s): {', '.join(missing)}")


def sha256_file(path: Path) -> str:
    if not path.is_file():
        raise ToolError(f"missing file for sha256: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def print_payload(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def ensure_not_accepted_baseline(output_root: Path) -> None:
    parts = output_root.resolve().parts
    if "F_FINAL_REVIEWED" in parts and "reproduction_runs" not in parts:
        raise ToolError(f"refusing accepted baseline output root: {output_root}")


def ensure_reproduction_sandbox(output_root: Path) -> None:
    if "reproduction_runs" not in output_root.resolve().parts:
        raise ToolError(f"--execute requires a reproduction sandbox output root containing reproduction_runs: {output_root}")


def validate_authority_path(value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"{label} authority path is required")
    raw = value.strip()
    for marker in FORBIDDEN_AUTHORITY_MARKERS:
        if marker in raw:
            raise ToolError(f"forbidden authority path for {label}: {raw}")
    path = Path(raw)
    if path.name in DERIVED_AUTHORITY_NAMES:
        raise ToolError(f"derived-only authority cannot be used as {label}: {raw}")
    if path.suffix.lower() in {".csv", ".yaml", ".yml"} and "input_snapshot" not in path.parts:
        raise ToolError(f"derived-only authority cannot be used as {label}: {raw}")
    return path


def resolve_output_root(cli_output_root: Path | None, manifest: dict[str, Any]) -> Path:
    if cli_output_root is not None:
        return cli_output_root
    raw = manifest.get("output_root")
    if not isinstance(raw, str) or not raw.strip():
        raise ToolError("missing required manifest field: output_root")
    return Path(raw)


def review_state_summary(state: dict[str, Any]) -> dict[str, int]:
    reviews = state.get("listeningReviewByKey") or state.get("listening_review_by_key") or {}
    if not isinstance(reviews, dict):
        reviews = {}
    review_items = [item for item in reviews.values() if isinstance(item, dict)]
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    alignments = state.get("phrase_alignments") or []
    if not isinstance(alignments, list):
        alignments = []
    event_ids = {
        str(item.get("event_id"))
        for item in alignments
        if isinstance(item, dict) and item.get("event_id")
    }
    phrase_ids = {
        str(item.get("phrase_id"))
        for item in alignments
        if isinstance(item, dict) and item.get("phrase_id")
    }
    if not phrase_ids:
        phrase_ids = {
            str(item.get("phrase_id"))
            for item in review_items
            if item.get("phrase_id")
        }
    return {
        "review_count": len(review_items),
        "preferred_version_count": len([value for value in preferred.values() if value]),
        "phrase_count": len(phrase_ids),
        "event_count": len(event_ids),
        "phrase_alignment_count": len(alignments),
    }
