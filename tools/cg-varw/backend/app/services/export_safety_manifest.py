from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPORT_CONTRACT_VERSION = "varw_export_contract.v0.1"
EXPORT_MANIFEST_NAME = "export_manifest.json"
FORBIDDEN_AUTHORITIES = ["Downloads", "browser Blob", "restore zip", "old exports", "archive copies"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_payload_hash(payload: Any) -> dict[str, str]:
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))
    return {"algorithm": "sha256", "source": "active_internal_state", "value": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def output_hashes(export_dir: Path, file_names: list[str]) -> list[dict[str, str]]:
    return [{"path": name, "algorithm": "sha256", "sha256": sha256_path(export_dir / name)} for name in file_names if (export_dir / name).exists()]


def row_counts(export_dir: Path, file_names: list[str]) -> dict[str, int]:
    return {name: len(read_csv_rows(export_dir / name)) for name in file_names if (export_dir / name).exists()}


def write_export_manifest(
    export_dir: Path,
    *,
    stage: str,
    canonical_source: str,
    input_payload: Any,
    file_names: list[str],
    generator: str,
    warnings: list[str],
    reload_validation: dict[str, Any],
    extra_fields: dict[str, Any] | None = None,
) -> Path:
    manifest = {
        "manifest_version": EXPORT_CONTRACT_VERSION,
        "stage": stage,
        "canonical_source": canonical_source,
        "canonical_source_role": "active_internal_state",
        "derived_export_only": True,
        "compatibility_export_only": True,
        "input_state_hash": stable_payload_hash(input_payload),
        "row_counts": row_counts(export_dir, file_names),
        "output_hashes": output_hashes(export_dir, file_names),
        "reload_validation": reload_validation,
        "forbidden_authority": FORBIDDEN_AUTHORITIES,
        "generated_at": now_iso(),
        "generator": generator,
        "warnings": warnings,
    }
    if extra_fields:
        manifest.update(extra_fields)
    path = export_dir / EXPORT_MANIFEST_NAME
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def read_manifest(export_dir: Path) -> dict[str, Any] | None:
    path = export_dir / EXPORT_MANIFEST_NAME
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def base_reload_validation(
    export_dir: Path,
    *,
    stage: str,
    validator: str,
    file_names: list[str],
    required_by_file: dict[str, tuple[str, ...]],
    expected_row_counts: dict[str, int] | None = None,
    expected_output_hashes: list[dict[str, str]] | None = None,
    extra_checks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    checked_at = now_iso()
    notes: list[str] = []
    checks: dict[str, Any] = {
        "stage": stage,
        "row_counts": {},
        "required_fields": {},
        "output_hashes": {},
        "canonical_authority_unchanged": True,
        "reload_is_export_consistency_only": True,
    }

    for name in file_names:
        path = export_dir / name
        if not path.exists():
            notes.append(f"missing file: {name}")
            continue
        try:
            rows = read_csv_rows(path)
        except Exception as exc:  # pragma: no cover - defensive manifest reporting
            notes.append(f"{name} parse error: {exc}")
            continue
        actual_count = len(rows)
        checks["row_counts"][name] = actual_count
        if expected_row_counts is not None and expected_row_counts.get(name) != actual_count:
            notes.append(f"{name} row_count mismatch: manifest={expected_row_counts.get(name)} actual={actual_count}")
        missing_fields = _missing_required_fields(name, rows, required_by_file.get(name, ()))
        checks["required_fields"][name] = "pass" if not missing_fields else missing_fields
        notes.extend(missing_fields)

    if expected_output_hashes is not None:
        expected_by_name = {item.get("path"): item.get("sha256") for item in expected_output_hashes if isinstance(item, dict)}
        for name in file_names:
            path = export_dir / name
            if not path.exists():
                continue
            actual_hash = sha256_path(path)
            checks["output_hashes"][name] = actual_hash
            if expected_by_name.get(name) != actual_hash:
                notes.append(f"output_hash stale: {name}")

    for check_name, check_value in (extra_checks or {}).items():
        checks[check_name] = check_value
        if isinstance(check_value, list):
            notes.extend(str(item) for item in check_value)

    return {
        "status": "fail" if notes else "pass",
        "validator": validator,
        "checked_at": checked_at,
        "checks": checks,
        "notes": notes,
    }


def _missing_required_fields(csv_name: str, rows: list[dict[str, str]], required: tuple[str, ...]) -> list[str]:
    notes: list[str] = []
    for row_index, row in enumerate(rows, start=1):
        for field in required:
            if row.get(field) in {"", None}:
                notes.append(f"{csv_name} row {row_index}: {field} missing")
    return notes
