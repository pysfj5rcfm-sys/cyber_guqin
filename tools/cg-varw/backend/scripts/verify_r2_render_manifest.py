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
    DERIVED_AUTHORITY_NAMES,
    ToolError,
    ensure_not_accepted_baseline,
    ensure_reproduction_sandbox,
    fail,
    load_json,
    load_json_compatible_yaml,
    print_payload,
    require_fields,
    review_state_summary,
    sha256_file,
    validate_authority_path,
)


COMMON_REQUIRED_FIELDS = [
    "piece_id",
    "session_id",
    "qinist_id",
    "source_review_state",
    "output_root",
    "dry_run_default",
    "forbid_overwrite_accepted_baseline",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only verifier for canonical R2 state and render manifests.")
    parser.add_argument("--review-state", required=True, type=Path)
    parser.add_argument("--render-manifest", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true", help="No-op flag for copy/paste symmetry; verifier is always read-only.")
    return parser.parse_args()


def validate_review_state_path(path: Path) -> None:
    validate_authority_path(str(path), "review_state")
    if path.name != "r2_review_state.latest.json":
        raise ToolError(f"review-state must be canonical r2_review_state.latest.json, got: {path}")
    if not path.is_file():
        raise ToolError(f"missing review-state file: {path}")


def manifest_required_fields(manifest: dict[str, Any]) -> list[str]:
    kind = str(manifest.get("manifest_kind") or manifest.get("render_kind") or "")
    if kind == "final_reviewed_render":
        return COMMON_REQUIRED_FIELDS + [
            "source_version",
            "target_version",
            "render_set_id",
            "input_snapshot_policy",
            "phrase_revision_policy",
            "tail_policy",
            "forbidden_authority",
            "sample_safety_rules",
            "reproduction_sandbox_required",
        ]
    if kind == "abcd_render":
        return COMMON_REQUIRED_FIELDS + [
            "render_set_id",
            "source_map",
            "phrase_plan",
            "version_policy",
            "output_versions",
            "tail_policy",
            "context_take_policy",
        ]
    return COMMON_REQUIRED_FIELDS


def validate_manifest(manifest: dict[str, Any]) -> None:
    require_fields(manifest, manifest_required_fields(manifest), "manifest")
    validate_authority_path(manifest.get("source_review_state"), "source_review_state")
    output_root = Path(str(manifest["output_root"]))
    ensure_not_accepted_baseline(output_root)
    if manifest.get("reproduction_sandbox_required") is True:
        ensure_reproduction_sandbox(output_root)
    if manifest.get("forbid_overwrite_accepted_baseline") is not True:
        raise ToolError("forbid_overwrite_accepted_baseline must be true")
    for field in ("source_map", "phrase_plan"):
        if field in manifest:
            validate_authority_path(str(manifest[field]), field)


def validate_derived_outputs_not_authority(manifest: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    derived = manifest.get("derived_outputs")
    if isinstance(derived, list):
        for item in derived:
            if isinstance(item, str) and Path(item).name in DERIVED_AUTHORITY_NAMES:
                notes.append(f"derived output registered as non-authority: {item}")
    return notes


def run(args: argparse.Namespace) -> int:
    validate_review_state_path(args.review_state)
    state = load_json(args.review_state)
    manifest = load_json_compatible_yaml(args.render_manifest)
    validate_manifest(manifest)
    notes = validate_derived_outputs_not_authority(manifest)
    payload = {
        "status": "PASS",
        "read_only": True,
        "review_state": str(args.review_state),
        "review_state_sha256": sha256_file(args.review_state),
        "render_manifest": str(args.render_manifest),
        "canonical_latest_json": True,
        "derived_csv_yaml_authority": False,
        "accepted_baseline_protected": True,
        "forbidden_authority_checked": True,
        "summary": review_state_summary(state),
        "notes": notes,
    }
    print_payload(payload)
    return 0


def main() -> int:
    try:
        return run(parse_args())
    except ToolError as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
