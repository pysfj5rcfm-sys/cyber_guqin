from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from cyber_guqin_reproduction_lib import (  # noqa: E402
    ToolError,
    ensure_not_accepted_baseline,
    ensure_reproduction_sandbox,
    fail,
    load_json,
    load_json_compatible_yaml,
    print_payload,
    require_fields,
    resolve_output_root,
    review_state_summary,
    sha256_file,
    validate_authority_path,
    write_csv,
    write_json,
)


REQUIRED_FIELDS = [
    "piece_id",
    "session_id",
    "qinist_id",
    "source_review_state",
    "source_version",
    "target_version",
    "output_root",
    "render_set_id",
    "input_snapshot_policy",
    "phrase_revision_policy",
    "tail_policy",
    "forbidden_authority",
    "sample_safety_rules",
    "dry_run_default",
    "forbid_overwrite_accepted_baseline",
    "reproduction_sandbox_required",
]

ALIGNMENT_FIELDS = [
    "target_version",
    "source_version",
    "render_set_id",
    "phrase_id",
    "planned_revision",
    "tail_policy",
    "target_output_root",
    "experimental_render",
    "production_grade",
    "not_sample_assets",
    "not_recording_segments",
    "not_ml_training_data",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__ or "Generate a sandbox final-reviewed render plan.")
    parser.add_argument("--final-render-manifest", required=True, type=Path)
    parser.add_argument("--output-root", type=Path, help="Override manifest output_root.")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print authority/render plan without writing.")
    parser.add_argument("--execute", action="store_true", help="Write sandbox metadata artifacts. Defaults to dry-run.")
    return parser.parse_args()


def validate_manifest(manifest: dict[str, Any], output_root: Path, execute: bool) -> Path:
    require_fields(manifest, REQUIRED_FIELDS, "manifest")
    if manifest.get("forbid_overwrite_accepted_baseline") is not True:
        raise ToolError("forbid_overwrite_accepted_baseline must be true")
    if manifest.get("reproduction_sandbox_required") is not True:
        raise ToolError("reproduction_sandbox_required must be true")
    source_path = validate_authority_path(manifest.get("source_review_state"), "source_review_state")
    ensure_not_accepted_baseline(output_root)
    if execute:
        ensure_reproduction_sandbox(output_root)
        if manifest.get("allow_execute") is not True:
            raise ToolError("manifest must set allow_execute=true before --execute can write sandbox artifacts")
    return source_path


def source_state(source_path: Path) -> dict[str, Any]:
    return load_json(source_path)


def planned_files(output_root: Path, target_version: str) -> dict[str, str]:
    return {
        "target_wav_planned": str(output_root / f"{target_version}.wav"),
        "alignment_csv": str(output_root / f"render_event_alignment.{target_version}.csv"),
        "render_report": str(output_root / f"{target_version}.sandbox_render_report.md"),
        "validation_json": str(output_root / f"{target_version}.sandbox_validation.json"),
        "input_snapshot": str(output_root / "input_snapshot" / "source_review_state.input_snapshot.json"),
    }


def planned_alignment_rows(manifest: dict[str, Any], state: dict[str, Any], output_root: Path) -> list[dict[str, str]]:
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    phrase_ids = sorted(str(key) for key in preferred) or ["MANIFEST_PHRASE_001"]
    policy = manifest.get("phrase_revision_policy")
    if not isinstance(policy, dict):
        policy = {}
    rows: list[dict[str, str]] = []
    for phrase_id in phrase_ids:
        rows.append(
            {
                "target_version": str(manifest["target_version"]),
                "source_version": str(manifest["source_version"]),
                "render_set_id": str(manifest["render_set_id"]),
                "phrase_id": phrase_id,
                "planned_revision": str(policy.get("default_intent", "preserve_reviewed_intent")),
                "tail_policy": str(manifest.get("tail_policy", "")),
                "target_output_root": str(output_root),
                "experimental_render": "true",
                "production_grade": "false",
                "not_sample_assets": "true",
                "not_recording_segments": "true",
                "not_ml_training_data": "true",
            }
        )
    return rows


def run(args: argparse.Namespace) -> int:
    manifest = load_json_compatible_yaml(args.final_render_manifest)
    output_root = resolve_output_root(args.output_root, manifest)
    source_path = validate_manifest(manifest, output_root, execute=args.execute)
    state = source_state(source_path)
    source_hash = sha256_file(source_path)
    summary = review_state_summary(state)
    files = planned_files(output_root, str(manifest["target_version"]))
    rows = planned_alignment_rows(manifest, state, output_root)
    payload = {
        "piece_id": manifest.get("piece_id"),
        "session_id": manifest.get("session_id"),
        "qinist_id": manifest.get("qinist_id"),
        "render_set_id": manifest.get("render_set_id"),
        "mode": "execute" if args.execute else "dry-run",
        "authority_summary": {
            "source_review_state": str(source_path),
            "source_review_hash": source_hash,
            "source_version": manifest.get("source_version"),
            "target_version": manifest.get("target_version"),
            **summary,
        },
        "planned_target_files": files,
        "sample_safety_checks": manifest.get("sample_safety_rules"),
        "warning_list": [
            "this generic tool does not run a real audio renderer",
            "writes are blocked unless --execute and reproduction sandbox are both present",
        ],
        "alignment_row_count": len(rows),
    }

    if not args.execute:
        print_payload({"status": "DRY_RUN", **payload})
        return 0

    output_root.mkdir(parents=True, exist_ok=True)
    write_csv(output_root / f"render_event_alignment.{manifest['target_version']}.csv", ALIGNMENT_FIELDS, rows)
    write_json(output_root / f"{manifest['target_version']}.sandbox_validation.json", payload)
    snapshot_dir = output_root / "input_snapshot"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    (snapshot_dir / "source_review_state.input_snapshot.json").write_bytes(source_path.read_bytes())
    (snapshot_dir / "source_review_state.input_snapshot.sha256").write_text(source_hash + "\n", encoding="utf-8")
    (output_root / f"{manifest['target_version']}.sandbox_render_report.md").write_text(
        "# Final Reviewed Sandbox Render Report\n\n"
        "No real audio render was run. This sandbox execute materialized authority, "
        "alignment-planning, validation, and input-snapshot artifacts only.\n",
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
