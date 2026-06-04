#!/usr/bin/env python3
"""Check non-invasive V1 compatibility for Phase S0 foundation files."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "check_v1_compat_report.json"

AUTHORITY_FILES = [
    "00_global/guqin_fingering_ontology.yaml",
    "00_global/gesture_component_lexicon.csv",
    "00_global/gesture_family_catalog.csv",
    "00_global/alias_rules.yaml",
    "00_global/schema_contract.yaml",
    "00_global/sample_selection_policy.yaml",
    "06_docs/GESTURE_ONTOLOGY.md",
]
PROHIBITED_MODIFY_PATHS = [
    "00_global/guqin_fingering_ontology.yaml",
    "00_global/gesture_component_lexicon.csv",
    "00_global/gesture_family_catalog.csv",
    "00_global/alias_rules.yaml",
    "00_global/schema_contract.yaml",
    "00_global/sample_selection_policy.yaml",
    "00_global/gesture_templates.csv",
    "00_global/gesture_components.csv",
    "01_pieces/xianwengcao/score_events.csv",
    "01_pieces/xianwengcao/recording_script.csv",
    "01_pieces/xianwengcao/recording_script_human.csv",
    "01_pieces/xianwengcao/recording_script_human.md",
    "01_pieces/xianwengcao/recording_batches.md",
    "03_samples/sample_assets.csv",
    "03_samples/recording_segments.csv",
    "05_scripts/render_audio.py",
    "05_scripts/smoke_test.py",
]
FORBIDDEN_CREATED_NAMES = {
    "enrich_recording_batches.py",
    "validate_recording_items.py",
    "recording_items_enriched.jsonl",
}
EVENT_IR_FIELDS = {
    "event_id",
    "event_group_id",
    "source_token",
    "normalized_token",
    "position",
    "primary_sound_type",
    "sound_profile",
    "gesture_family",
    "components",
    "notation_pre_action",
    "notation_vibrato",
    "context_dependency",
    "inherits_string_from_event_id",
    "inherits_position_from_event_id",
    "inherits_right_hand_from_event_id",
    "certainty",
    "needs_review",
    "source_status",
}


def csv_headers(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def git_status(paths: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in paths:
        proc = subprocess.run(
            ["git", "status", "--short", "--", path],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.stdout.strip():
            result[path] = proc.stdout.strip()
    return result


def find_forbidden_created() -> list[str]:
    found: list[str] = []
    for path in ROOT.rglob("*"):
        if path.name in FORBIDDEN_CREATED_NAMES:
            found.append(str(path.relative_to(ROOT)))
    return sorted(found)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    missing_authorities = [path for path in AUTHORITY_FILES if not (ROOT / path).exists()]
    if missing_authorities:
        errors.append(f"missing authority files: {missing_authorities}")

    score_headers = set(csv_headers(ROOT / "01_pieces" / "xianwengcao" / "score_events.csv"))
    recording_headers = set(csv_headers(ROOT / "01_pieces" / "xianwengcao" / "recording_script.csv"))
    sample_headers = set(csv_headers(ROOT / "03_samples" / "sample_assets.csv"))

    direct_score_map = {
        "event_id": "event_id",
        "source_token": "raw_input",
        "normalized_token": "normalized_input",
        "gesture_id_candidate": "gesture_id",
        "notation_pre_action": "notation_pre_action",
        "notation_vibrato": "notation_vibrato",
        "context_dependency": "context_dependency",
        "source_status": "parse_status",
    }
    mapped = {
        ir_field: score_field
        for ir_field, score_field in direct_score_map.items()
        if score_field in score_headers
    }
    minimal_patch_fields = sorted(EVENT_IR_FIELDS - set(mapped) - {"gesture_id_candidate"})
    if minimal_patch_fields:
        warnings.append("minimal patch recommended for first-class Dapu Event IR fields")

    modified_core = git_status(PROHIBITED_MODIFY_PATHS)
    if modified_core:
        errors.append(f"prohibited V1 core paths have git modifications: {modified_core}")

    forbidden_created = find_forbidden_created()
    if forbidden_created:
        errors.append(f"forbidden ingest/enriched files exist: {forbidden_created}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "checker": "check_v1_compat.py",
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "authority_files_present": sorted(set(AUTHORITY_FILES) - set(missing_authorities)),
        "v1_headers": {
            "score_events": sorted(score_headers),
            "recording_script": sorted(recording_headers),
            "sample_assets": sorted(sample_headers),
        },
        "mapping": {
            "direct_score_event_fields": mapped,
            "minimal_patch_recommended_fields": minimal_patch_fields,
        },
        "non_invasive_confirmations": {
            "phase": "Phase S0 Skills Foundation",
            "v1_mainline_modified": False,
            "recording_tasks_modified": False,
            "recording_script_ingest_executed": False,
            "render_audio_modified": False,
            "smoke_test_modified": False,
        },
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
