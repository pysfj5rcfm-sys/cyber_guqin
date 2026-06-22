#!/usr/bin/env python3
"""Plan or materialize sandbox ABCD render artifacts from a manifest.

This generic entry point validates source maps, phrase plans, version policy,
and output names without using any piece-specific constants. Dry-run is the
default and never writes audio.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from cyber_guqin_reproduction_lib import (
    ToolError,
    ensure_not_accepted_baseline,
    ensure_reproduction_sandbox,
    fail,
    load_json_compatible_yaml,
    print_payload,
    require_fields,
    resolve_output_root,
    write_csv,
    write_json,
)


REQUIRED_FIELDS = [
    "piece_id",
    "session_id",
    "qinist_id",
    "render_set_id",
    "source_map",
    "phrase_plan",
    "version_policy",
    "output_versions",
    "tail_policy",
    "context_take_policy",
    "output_root",
    "dry_run_default",
    "forbid_overwrite_accepted_baseline",
]

ALIGNMENT_FIELDS = [
    "version_id",
    "phrase_id",
    "event_id",
    "source_ref",
    "target_output_path",
    "tail_policy",
    "context_take_policy",
    "experimental_render",
    "production_grade",
    "not_sample_assets",
    "not_recording_segments",
    "not_ml_training_data",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render-manifest", required=True, type=Path)
    parser.add_argument("--output-root", type=Path, help="Override manifest output_root.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print planned paths without writing.")
    parser.add_argument("--execute", action="store_true", help="Write sandbox metadata artifacts. Defaults to dry-run.")
    return parser.parse_args()


def normalize_versions(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    versions = manifest.get("output_versions")
    if not isinstance(versions, dict) or not versions:
        raise ToolError("missing required manifest field: output_versions")
    normalized: dict[str, dict[str, Any]] = {}
    for version_id, spec in versions.items():
        if not isinstance(spec, dict):
            raise ToolError(f"output_versions.{version_id} must be an object")
        output_name = spec.get("output_name")
        if not output_name:
            raise ToolError(f"output_versions.{version_id}.output_name is required")
        normalized[str(version_id)] = spec
    return normalized


def validate_manifest(manifest: dict[str, Any], output_root: Path, execute: bool) -> dict[str, dict[str, Any]]:
    require_fields(manifest, REQUIRED_FIELDS, "manifest")
    if manifest.get("forbid_overwrite_accepted_baseline") is not True:
        raise ToolError("forbid_overwrite_accepted_baseline must be true")
    for field in ("source_map", "phrase_plan"):
        value = str(manifest.get(field) or "")
        if any(marker in value for marker in ("Downloads", "browser Blob", "browser_Blob", "restore zip", "restore_zip", ".zip")):
            raise ToolError(f"forbidden authority path for {field}: {value}")
    if not isinstance(manifest.get("version_policy"), dict):
        raise ToolError("missing required manifest field: version_policy")
    versions = normalize_versions(manifest)
    ensure_not_accepted_baseline(output_root)
    if execute:
        ensure_reproduction_sandbox(output_root)
    return versions


def planned_paths(output_root: Path, versions: dict[str, dict[str, Any]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for version_id, spec in versions.items():
        version_dir = output_root / version_id
        result[version_id] = {
            "planned_wav_path": str(version_dir / str(spec["output_name"])),
            "alignment_csv": str(version_dir / f"render_event_alignment.{version_id}.csv"),
            "version_report": str(version_dir / f"{version_id}.sandbox_render_report.md"),
        }
    return result


def alignment_rows(manifest: dict[str, Any], output_root: Path, versions: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    phrase_plan = manifest.get("phrase_plan_items")
    if not isinstance(phrase_plan, list) or not phrase_plan:
        phrase_plan = [{"phrase_id": "MANIFEST_PHRASE_001", "event_id": "MANIFEST_EVENT_001", "source_ref": "manifest_source_map"}]
    rows: list[dict[str, str]] = []
    paths = planned_paths(output_root, versions)
    for version_id in versions:
        for item in phrase_plan:
            if not isinstance(item, dict):
                continue
            rows.append(
                {
                    "version_id": version_id,
                    "phrase_id": str(item.get("phrase_id", "")),
                    "event_id": str(item.get("event_id", "")),
                    "source_ref": str(item.get("source_ref", manifest.get("source_map", ""))),
                    "target_output_path": paths[version_id]["planned_wav_path"],
                    "tail_policy": str(manifest.get("tail_policy", "")),
                    "context_take_policy": str(manifest.get("context_take_policy", "")),
                    "experimental_render": "true",
                    "production_grade": "false",
                    "not_sample_assets": "true",
                    "not_recording_segments": "true",
                    "not_ml_training_data": "true",
                }
            )
    return rows


def run(args: argparse.Namespace) -> int:
    manifest = load_json_compatible_yaml(args.render_manifest)
    output_root = resolve_output_root(args.output_root, manifest)
    versions = validate_manifest(manifest, output_root, execute=args.execute)
    paths = planned_paths(output_root, versions)
    rows = alignment_rows(manifest, output_root, versions)
    payload = {
        "piece_id": manifest.get("piece_id"),
        "session_id": manifest.get("session_id"),
        "qinist_id": manifest.get("qinist_id"),
        "render_set_id": manifest.get("render_set_id"),
        "mode": "execute" if args.execute else "dry-run",
        "planned_output_paths": paths,
        "alignment_row_count": len(rows),
        "warnings": [
            "this generic tool does not run a real audio renderer",
            "sandbox artifacts are not sample ingest and not ML training data",
        ],
    }

    if not args.execute:
        print_payload({"status": "DRY_RUN", **payload})
        return 0

    output_root.mkdir(parents=True, exist_ok=True)
    write_json(output_root / "abcd_render_manifest.sandbox.json", {"manifest": manifest, **payload})
    write_csv(output_root / "render_event_alignment.sandbox.csv", ALIGNMENT_FIELDS, rows)
    (output_root / "README_NO_REAL_AUDIO_RENDER.md").write_text(
        "# ABCD Sandbox Execute\n\n"
        "This directory was produced by the generic dry-run-first ABCD tool. "
        "It materializes metadata and alignment planning only; no real audio render was run.\n",
        encoding="utf-8",
    )
    print_payload({"status": "EXECUTE_WRITTEN", **payload})
    return 0


def main() -> int:
    try:
        return run(parse_args())
    except ToolError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
