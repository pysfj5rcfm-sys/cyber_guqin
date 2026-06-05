#!/usr/bin/env python3
"""Audit Cyber Guqin recording/sample ingest readiness.

This script is intentionally read-only for V1 runtime data. It only writes the
Phase 1B-R0 audit reports under reports/.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"

REPORT_MD = REPORT_DIR / "recording_ingest_readiness.md"
REPORT_JSON = REPORT_DIR / "recording_ingest_field_gap.json"
REPORT_NEXT = REPORT_DIR / "recording_ingest_next_steps.md"
REPORT_DECISIONS = REPORT_DIR / "recording_ingest_decisions_needed.md"

FILES_TO_CHECK = [
    "00_global/qinists.csv",
    "00_global/pieces.csv",
    "00_global/qins.csv",
    "00_global/tunings.csv",
    "00_global/gesture_templates.csv",
    "00_global/gesture_components.csv",
    "00_global/schema_contract.yaml",
    "00_global/parse_rules.yaml",
    "00_global/guqin_fingering_ontology.yaml",
    "00_global/gesture_component_lexicon.csv",
    "00_global/gesture_family_catalog.csv",
    "00_global/alias_rules.yaml",
    "00_global/sample_selection_policy.yaml",
    "01_pieces/xianwengcao/score_events.csv",
    "01_pieces/xianwengcao/phrase_structure.csv",
    "01_pieces/xianwengcao/recording_script.csv",
    "01_pieces/xianwengcao/recording_script_human.csv",
    "01_pieces/xianwengcao/recording_script_human.md",
    "01_pieces/xianwengcao/recording_batches.md",
    "01_pieces/xianwengcao/rhythm_candidates",
    "01_pieces/xianwengcao/reviews",
    "02_recordings/recording_sessions.csv",
    "02_recordings/raw_audio",
    "03_samples/recording_segments.csv",
    "03_samples/sample_assets.csv",
    "03_samples/QIN_A/ZHENG_DIAO",
    "05_scripts/generate_recording_script.py",
    "05_scripts/export_recording_checklist.py",
    "05_scripts/make_dummy_samples.py",
    "05_scripts/generate_rhythm.py",
    "05_scripts/render_audio.py",
    "05_scripts/audio_viability_review.py",
    "05_scripts/smoke_test.py",
    ".agents/skills/guqin-canon-builder/SKILL.md",
    ".agents/skills/guqin-dapu-parser/SKILL.md",
    "canon/sources.yaml",
    "canon/terms.yaml",
    "canon/component_lexicon.yaml",
    "canon/gesture_families.yaml",
    "canon/alias_rules.yaml",
    "canon/technique_rules.yaml",
    "canon/validation_rules.yaml",
    "canon/drafts/qxby_batch_001.yaml",
    "canon/drafts/qxby_batch_002.yaml",
    "scripts/validate_canon.py",
    "scripts/validate_dapu_ir.py",
    "scripts/check_v1_compat.py",
    "scripts/validate_canon_seed.py",
    "scripts/validate_qxby_batch.py",
    "scripts/audit_qxby_batch_sources.py",
    "scripts/audit_v1_to_canon_coverage.py",
    "06_docs/GESTURE_ONTOLOGY.md",
    "06_docs/PROJECT_STRUCTURE.md",
    "reports/REPORTS_INDEX.md",
    "reports/v1_to_canon_coverage.md",
    "reports/qxby_batch_002_collection_plan.md",
    "reports/qxby_batch_001_human_review.md",
    "reports/qxby_batch_002_report.md",
    "reports/validator_parameterization_report.md",
]

RECORDING_SCRIPT_REQUIRED = {
    "script_id",
    "recording_id",
    "order_no",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "realization_pre_action",
    "realization_vibrato",
}

HUMAN_SCRIPT_REQUIRED = {
    "batch_take_no",
    "recording_take_no",
    "order_no",
    "script_id",
    "event_id",
    "event_range",
    "normalized_name",
    "gesture_id",
    "expected_sample_type",
    "realization_variant",
    "realization_pre_action",
    "realization_vibrato",
    "human_instruction",
}

SESSION_RECOMMENDED = [
    "recording_session_id",
    "qinist_id",
    "qin_id",
    "tuning_id",
    "piece_id",
    "recording_id",
    "date",
    "location",
    "recorder",
    "microphone",
    "audio_interface",
    "sample_rate",
    "bit_depth",
    "channel_count",
    "file_format",
    "room_noise_note",
    "qin_condition_note",
    "recording_mode",
    "source_raw_files",
    "linked_recording_script",
    "notes",
]

TAKE_MANIFEST_FIELDS = [
    "recording_session_id",
    "recording_id",
    "recording_take_no",
    "batch_take_no",
    "script_id",
    "event_id",
    "event_range",
    "gesture_id",
    "normalized_name",
    "expected_sample_type",
    "realization_variant",
    "source_raw_file",
    "take_start_time",
    "take_end_time",
    "take_quality",
    "performer_note",
    "engineer_note",
    "needs_reshoot",
    "selected_for_sample",
    "notes",
]

SEGMENT_RECOMMENDED = [
    "segment_id",
    "recording_session_id",
    "recording_id",
    "source_raw_file",
    "source_take_id",
    "script_id",
    "event_id",
    "event_range",
    "gesture_id",
    "sample_type",
    "realization_variant",
    "start_time_s",
    "end_time_s",
    "attack_marker_ms",
    "release_tail_ms",
    "file_path",
    "extraction_method",
    "qc_status",
    "notes",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def checked_files() -> list[dict[str, Any]]:
    rows = []
    for item in FILES_TO_CHECK:
        path = ROOT / item
        rows.append(
            {
                "path": item,
                "exists": path.exists(),
                "kind": "directory" if path.is_dir() else "file",
                "status": "present"
                if path.exists()
                else ("expected_missing_this_phase" if item.endswith(("raw_audio", "reviews")) else "missing"),
            }
        )
    return rows


def add_gap(gaps: list[dict[str, str]], area: str, field: str, severity: str, status: str, recommendation: str) -> None:
    gaps.append(
        {
            "area": area,
            "field": field,
            "severity": severity,
            "current_status": status,
            "recommendation": recommendation,
        }
    )


def count_nonempty(rows: list[dict[str, str]], field: str) -> int:
    return sum(1 for row in rows if row.get(field))


def summarize_rows() -> dict[str, Any]:
    headers: dict[str, list[str]] = {}
    tables: dict[str, list[dict[str, str]]] = {}
    for name, path in {
        "score_events": ROOT / "01_pieces/xianwengcao/score_events.csv",
        "recording_script": ROOT / "01_pieces/xianwengcao/recording_script.csv",
        "recording_script_human": ROOT / "01_pieces/xianwengcao/recording_script_human.csv",
        "recording_sessions": ROOT / "02_recordings/recording_sessions.csv",
        "recording_segments": ROOT / "03_samples/recording_segments.csv",
        "sample_assets": ROOT / "03_samples/sample_assets.csv",
        "gesture_templates": ROOT / "00_global/gesture_templates.csv",
        "gesture_components": ROOT / "00_global/gesture_components.csv",
    }.items():
        header, rows = read_csv(path)
        headers[name] = header
        tables[name] = rows

    script = tables["recording_script"]
    human = tables["recording_script_human"]
    assets = tables["sample_assets"]
    score = tables["score_events"]
    templates = tables["gesture_templates"]

    context_rows = [r for r in human if r.get("expected_sample_type") == "context" or r.get("realization_variant") == "context"]
    instruction_text = "\n".join((r.get("human_instruction", "") + " " + r.get("notes", "")) for r in human)

    return {
        "headers": headers,
        "tables": tables,
        "counts": {
            "score_events": len(score),
            "gesture_templates": len(templates),
            "gesture_components": len(tables["gesture_components"]),
            "recording_script": len(script),
            "recording_script_human": len(human),
            "recording_sessions": len(tables["recording_sessions"]),
            "recording_segments": len(tables["recording_segments"]),
            "sample_assets": len(assets),
        },
        "script_summary": {
            "expected_total_takes": len(human) if human else len(script),
            "atomic_take_count": sum(
                1 for r in human if r.get("expected_sample_type") == "atomic" and r.get("realization_variant") != "context"
            ),
            "context_take_count": len(context_rows),
            "variant_types": sorted(set(r.get("realization_variant", "") for r in human if r.get("realization_variant"))),
            "sample_types": dict(Counter(r.get("expected_sample_type", "") for r in human)),
            "realization_pre_actions": dict(Counter(r.get("realization_pre_action", "") for r in human)),
            "context_rows_without_event_range": sum(1 for r in context_rows if not r.get("event_range")),
            "has_key_instruction_qifen": "七徽九分" in instruction_text,
            "has_key_instruction_dazhu": "大注九勾四撞" in instruction_text,
            "has_key_instruction_qiaqi_context": "掐起 context" in instruction_text or "上下文版本" in instruction_text,
            "has_key_instruction_zhuang_to_qiaqi": "撞到掐起" in instruction_text or "撞—掐起" in instruction_text,
        },
        "asset_summary": {
            "source_types": dict(Counter(r.get("source_type", "") for r in assets)),
            "sample_types": dict(Counter(r.get("sample_type", "") for r in assets)),
            "variant_types": dict(Counter(r.get("realization_variant", "") for r in assets)),
            "quality_statuses": dict(Counter(r.get("quality_status", "") for r in assets)),
            "source_segment_empty_count": sum(1 for r in assets if not r.get("source_segment_id")),
            "source_event_range_count": count_nonempty(assets, "source_event_range"),
            "sample_rates": dict(Counter(r.get("sample_rate", "") for r in assets)),
            "bit_depths": dict(Counter(r.get("bit_depth", "") for r in assets)),
        },
    }


def build_gap_report(summary: dict[str, Any], files: list[dict[str, Any]]) -> dict[str, Any]:
    headers = summary["headers"]
    counts = summary["counts"]
    script_summary = summary["script_summary"]
    gaps: list[dict[str, str]] = []

    script_missing = sorted(RECORDING_SCRIPT_REQUIRED - set(headers["recording_script"]))
    human_missing = sorted(HUMAN_SCRIPT_REQUIRED - set(headers["recording_script_human"]))
    for field in script_missing:
        add_gap(gaps, "recording_script", field, "must_before_recording", "missing", "Add before using the structured script as a real recording source.")
    for field in human_missing:
        add_gap(gaps, "recording_script_human", field, "must_before_recording", "missing", "Add before issuing the human recording checklist.")

    if script_summary["expected_total_takes"] != 71:
        add_gap(gaps, "recording_script_human", "row_count", "must_before_recording", f"got {script_summary['expected_total_takes']}", "Expected 71 recording tasks for XWC Phase 1A.")

    if script_summary["context_rows_without_event_range"]:
        add_gap(
            gaps,
            "recording_script_human",
            "event_range",
            "must_before_splitting",
            f"{script_summary['context_rows_without_event_range']} context row(s) lack event_range",
            "Fill event_range for every context take before cutting or registering real segments.",
        )

    if "context" not in script_summary["variant_types"]:
        add_gap(gaps, "recording_script_human", "realization_variant", "must_before_recording", "context variant absent", "Context takes need explicit variant marking.")

    session_headers = set(headers["recording_sessions"])
    for field in SESSION_RECOMMENDED:
        if field not in session_headers:
            severity = "must_before_recording" if field in {
                "recording_session_id",
                "recording_mode",
                "sample_rate",
                "bit_depth",
                "channel_count",
                "file_format",
                "source_raw_files",
                "linked_recording_script",
            } else "optional"
            add_gap(gaps, "recording_sessions", field, severity, "missing", "Capture in a session manifest before real audio is archived.")

    for field in TAKE_MANIFEST_FIELDS:
        severity = "must_before_splitting" if field in {
            "recording_session_id",
            "recording_take_no",
            "script_id",
            "source_raw_file",
            "take_start_time",
            "take_end_time",
            "take_quality",
        } else "optional"
        add_gap(gaps, "take_manifest", field, severity, "no take manifest exists", "Create as a future manifest, not during this audit.")

    segment_headers = set(headers["recording_segments"])
    for field in SEGMENT_RECOMMENDED:
        if field not in segment_headers:
            severity = "must_before_splitting" if field in {
                "recording_session_id",
                "source_raw_file",
                "source_take_id",
                "script_id",
                "event_range",
                "gesture_id",
                "sample_type",
                "realization_variant",
                "start_time_s",
                "end_time_s",
                "file_path",
                "qc_status",
            } else "should_before_render"
            add_gap(gaps, "recording_segments", field, severity, "missing", "Add before registering real audio slices.")

    asset_headers = set(headers["sample_assets"])
    for field in ["sample_version", "selected_sample_set", "active_sample_set"]:
        add_gap(gaps, "sample_assets", field, "should_before_render", "missing", "Needed to manage real/dummy coexistence and render selection.")
    if "source_type" in asset_headers:
        add_gap(gaps, "sample_assets", "source_type", "must_before_splitting", "present, currently dummy only", "Allow dummy and real_recording values to coexist.")
    if "source_segment_id" in asset_headers:
        add_gap(gaps, "sample_assets", "source_segment_id", "must_before_splitting", "present, empty for all dummy rows", "Populate only after real recording_segments are registered.")

    missing_required_files = [
        f["path"]
        for f in files
        if not f["exists"] and f["status"] == "missing"
    ]

    readiness_status = "warning"
    if missing_required_files or script_missing or human_missing or counts["recording_script_human"] != 71:
        readiness_status = "fail"

    return {
        "audit_type": "recording_sample_ingest_readiness",
        "piece_id": "XWC",
        "qinist_id": "QINIST_001",
        "readiness_status": readiness_status,
        "checked_files": files,
        "recording_task_summary": {
            "expected_total_takes": script_summary["expected_total_takes"],
            "has_recording_script": (ROOT / "01_pieces/xianwengcao/recording_script.csv").exists(),
            "has_human_recording_script": (ROOT / "01_pieces/xianwengcao/recording_script_human.csv").exists(),
            "has_recording_batches": (ROOT / "01_pieces/xianwengcao/recording_batches.md").exists(),
            "atomic_take_count": script_summary["atomic_take_count"],
            "context_take_count": script_summary["context_take_count"],
            "variant_types": script_summary["variant_types"],
        },
        "field_gaps": gaps,
        "proposed_new_files": [
            {
                "path": "02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001/session_manifest.yaml",
                "purpose": "Capture session-level environment, equipment, format, and recording mode.",
                "create_now": False,
                "phase": "Phase 1B-1",
            },
            {
                "path": "02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001/take_manifest.csv",
                "purpose": "Map the 71 expected tasks to raw file boundaries, retakes, and quality choices.",
                "create_now": False,
                "phase": "Phase 1B-2",
            },
            {
                "path": "05_scripts/split_recording_session.py",
                "purpose": "Future manual/semi-auto splitter from raw WAV plus take manifest into segments.",
                "create_now": False,
                "phase": "Phase 1B-3",
            },
            {
                "path": "05_scripts/ingest_recording_segments.py",
                "purpose": "Future runtime-side registration of verified segment rows.",
                "create_now": False,
                "phase": "Phase 1B-3",
            },
            {
                "path": "05_scripts/promote_segments_to_samples.py",
                "purpose": "Future promotion from good segments to real sample_assets and sample sets.",
                "create_now": False,
                "phase": "Phase 1B-5",
            },
        ],
        "do_not_create_now": [
            "real audio slices",
            "recording_items_enriched.jsonl",
            "recording ingest data rows",
            "V1 patch scripts",
            "machine learning training scripts",
            "OCR pipeline outputs",
            "new canon drafts",
            "real sample_assets rows",
            "real recording_segments rows",
        ],
        "risks": [
            "Context takes without explicit event_range can lose the relationship between source event, inherited event, and sample.",
            "Using batch order as score order would scramble event chronology; keep batch_take_no separate from score event order.",
            "Writing sample_assets before segment QC would hide rejected/bad takes and weaken provenance.",
            "Overwriting dummy assets instead of coexisting sample sets would make regression rendering harder.",
        ],
        "next_steps": [
            "Confirm session manifest fields and recording format before recording.",
            "Archive raw audio permanently as read-only originals, then make normalized copies.",
            "Create a take manifest from the 71 task script before cutting.",
            "Manually or semi-automatically split a small pilot batch before full 71-take ingest.",
            "Promote only good segments into a real sample set after QC.",
        ],
    }


def bullet(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def write_readiness_md(summary: dict[str, Any], gap_report: dict[str, Any]) -> None:
    counts = summary["counts"]
    script = summary["script_summary"]
    assets = summary["asset_summary"]
    headers = summary["headers"]
    status = gap_report["readiness_status"]

    section_lines = [
        "# Recording Sample Ingest Readiness Audit",
        "",
        "Scope: Phase 1B-R0 read-only audit. This report does not import audio, create slices, alter runtime data, patch V1, or generate enriched recording items.",
        "",
        "Validator handling: several existing validators write fixed files under reports/. To keep this audit from rewriting unrelated report artifacts, run those validators in a temporary workspace copy and record their command results in the execution summary.",
        "",
        "## 1. Executive Summary",
        "",
        f"Readiness status: {status}. The 71-task recording checklist is usable as the real recording execution source, but the system should not start slicing or sample_assets ingest until session and take manifests are added and the real segment schema is extended.",
        "",
        "Direct answers:",
        "",
        "- Can start recording now: yes, with a session manifest decision pass before the first take.",
        "- Can start slicing now: no; add take manifest and recording_segments provenance fields first.",
        "- Can write sample_assets now: no; real samples should enter through segments and QC first.",
        "- Need V1 minimal patch now: yes as a recommendation, not in this audit. The patch should target manifests/segment fields/sample-set selection.",
        "- Need recording_items_enriched now: no. Reserve it for a future semantic bridge after the recording archive is stable.",
        "- Prefer session manifest before slicing: yes.",
        "- Prefer manual or semi-auto slicing first: yes.",
        "- Preserve raw audio permanently read-only: yes.",
        "- Keep dummy and real samples together: yes, separated by source_type and sample set.",
        "- Let context samples drive first render: not yet; keep them for training/reference and special left-hand-sound cases until selection policy is explicit.",
        "- Pilot first: yes, ingest a small real batch before processing all 71 tasks.",
        "- Archive all 71 raw takes before slicing: yes, even if slicing starts with a pilot subset.",
        "",
        "## 2. Readiness Status",
        "",
        f"Status: {status}. Existing files support recording-day execution, but not lossless real sample ingest. This is a warning state rather than pass because field-level provenance is incomplete for recording sessions, take boundaries, segment QC, and sample-set selection.",
        "",
        "## 3. Current V1 Recording / Sample Structure Overview",
        "",
        f"- score_events.csv: {counts['score_events']} score facts.",
        f"- gesture_templates.csv: {counts['gesture_templates']} templates.",
        f"- gesture_components.csv: {counts['gesture_components']} components.",
        f"- recording_script.csv: {counts['recording_script']} structured recording tasks.",
        f"- recording_script_human.csv: {counts['recording_script_human']} human-facing tasks.",
        f"- recording_sessions.csv: {counts['recording_sessions']} rows and columns {headers['recording_sessions']}.",
        f"- recording_segments.csv: {counts['recording_segments']} rows and columns {headers['recording_segments']}.",
        f"- sample_assets.csv: {counts['sample_assets']} rows, source types {assets['source_types']}, sample types {assets['sample_types']}.",
        "- 02_recordings/raw_audio is absent, which is expected before real recording but means archive layout is not yet materialized.",
        "",
        "## 4. 71 Recording Task Check Results",
        "",
        f"- Total takes: {script['expected_total_takes']}.",
        f"- Atomic takes: {script['atomic_take_count']}.",
        f"- Context takes: {script['context_take_count']}.",
        f"- Variants: {', '.join(script['variant_types'])}.",
        "- script_id, recording_take_no, batch_take_no, event_id, gesture_id, expected_sample_type, realization_variant, and realization_pre_action are present in the human script.",
        "- Key instructions are preserved for 上滑至七徽九分, 大注九勾四撞, 掐起 context, and 撞到掐起 context.",
        f"- Context rows missing event_range: {script['context_rows_without_event_range']}. This is acceptable for recording-day reading, but not for slicing or ingest.",
        "- recording_take_no should be the stable whole-session take number. batch_take_no should remain the performer-facing order inside grouped batches. Neither should overwrite event_no or score order.",
        "- Main risk: recording_batches.md is an execution order view and must not be treated as score authority.",
        "",
        "## 5. Raw Audio Archive Recommendation",
        "",
        "Recommended structure, not created in this audit:",
        "",
        "```text",
        "02_recordings/",
        "├── recording_sessions.csv",
        "└── raw_audio/",
        "    └── QINIST_001/",
        "        └── XWC/",
        "            └── RS_XWC_001/",
        "                ├── raw/",
        "                ├── normalized/",
        "                ├── session_manifest.yaml",
        "                ├── take_manifest.csv",
        "                └── notes.md",
        "```",
        "",
        "- Recommended mode: record either batch-level continuous WAVs or 71 per-take WAVs. Batch-level continuous WAVs are usually safer for performance flow if every take boundary is captured in take_manifest.",
        "- If continuous: preserve take_start_time and take_end_time for each script_id, plus spoken slate policy.",
        "- If 71 files: use names like RS_XWC_001_TK001_RS_XWC_001_001_straight.wav and append _retake02 for retakes.",
        "- Preserve original raw files untouched forever; create normalized copies separately.",
        "- Recommended normalized format: WAV, 48 kHz or 44.1 kHz, 24-bit preferred for capture if available, mono if using one microphone and stereo only if placement is intentional.",
        "- Include recording environment metadata: room, noise note, recorder, microphone, interface, qin condition, tuning note, and reference tone/noise samples.",
        "",
        "## 6. Recording Session Manifest Recommendation",
        "",
        "Recommended fields:",
        "",
        *bullet(SESSION_RECOMMENDED),
        "",
        "Current recording_sessions.csv is only a high-level placeholder. Fields that must be fixed before recording are recording_session_id, recording_mode, sample_rate, bit_depth, channel_count, file_format, source_raw_files, and linked_recording_script. Location/equipment notes can be partly backfilled, but it is safer to capture them at the session.",
        "",
        "## 7. Take Manifest Recommendation",
        "",
        "A take manifest is needed before slicing. Prefer colocating it with the raw session folder, e.g. 02_recordings/raw_audio/QINIST_001/XWC/RS_XWC_001/take_manifest.csv, because it travels with the raw archive.",
        "",
        "Recommended fields:",
        "",
        *bullet(TAKE_MANIFEST_FIELDS),
        "",
        "- Convert the 71 recording tasks into expected takes before or immediately after recording.",
        "- A take may map to multiple events via event_range, especially context takes.",
        "- Bad takes and retakes should remain in the manifest with take_quality, needs_reshoot, and selected_for_sample.",
        "- Keep take_no and script_id together: take_no tracks physical recording order; script_id tracks intended semantic task.",
        "",
        "## 8. recording_segments.csv Field Gaps",
        "",
        f"Current fields: {headers['recording_segments']}. This is insufficient for real audio slicing.",
        "",
        "Recommended fields:",
        "",
        *bullet(SEGMENT_RECOMMENDED),
        "",
        "- Keep both source_take_id and event_id/event_range so a segment can be traced to raw audio and score semantics.",
        "- Context samples require event_range.",
        "- straight/chuo/zhu belongs in realization_variant or realization_pre_action, not in score facts.",
        "- attack_marker_ms should be manually checked at first; release_tail_ms should be retained for natural decay.",
        "- Distinguish take segments from final samples: recording_segments is source evidence; sample_assets is promoted usable material.",
        "",
        "## 9. sample_assets.csv Field Gaps",
        "",
        f"Current source types: {assets['source_types']}. Current quality statuses: {assets['quality_statuses']}.",
        "",
        "- Dummy and real samples should coexist through source_type=dummy and source_type=real_recording.",
        "- Existing source_recording_id/source_segment_id/source_event_id/source_event_range fields are a good start, but real rows need populated source_segment_id.",
        "- realization_variant and realization_pre_action already exist and should carry straight/chuo/zhu realization facts.",
        "- sample_type covers atomic/context, but context should not automatically enter first-version render without policy.",
        "- Add sample_version and selected_sample_set/active_sample_set concepts before real render selection.",
        "- Preserve multiple takes in sample_assets or a linked segment table; do not overwrite earlier takes when choosing active samples.",
        "",
        "## 10. straight / chuo / zhu / context Take Handling",
        "",
        "- straight: direct baseline realization, useful as fallback and comparison.",
        "- chuo: Sanman default for unmarked pressed notes; keep as realization_pre_action=chuo, never as score notation unless explicitly marked.",
        "- zhu: use for score-marked 注 and prioritize it when notation_pre_action=zhu.",
        "- context: record as independent evidence, especially for 掐起 and 撞到掐起 transitions. Promote only after event_range and selection policy are explicit.",
        "- default_chuo/no_chuo should remain realization/sample-selection concepts, separated from score_events.",
        "",
        "## 11. Split Workflow Recommendation",
        "",
        "- 05_scripts/ is appropriate for future V1 runtime pipeline scripts that transform real recording data into V1 sample tables.",
        "- scripts/ should remain for audits, validators, canon utilities, and read-only checks.",
        "- Future split_recording_session.py is useful, but should be created after manifests are agreed.",
        "- Start with manual or semi-auto split using Audacity/Reaper timestamp exports.",
        "- Support both long WAV + take_manifest and per-take WAV registration.",
        "- Suggested future scripts: 05_scripts/split_recording_session.py, 05_scripts/ingest_recording_segments.py, 05_scripts/promote_segments_to_samples.py.",
        "",
        "## 12. Dapu Event IR / Skills Bridge Recommendation",
        "",
        "- recording ingest should not depend on dapu-parser for raw audio archiving.",
        "- score facts come from score_events.csv and gesture templates/components.",
        "- performance realization comes from realization_variant, realization_pre_action, qinist profile, and sample selection policy.",
        "- recording execution comes from recording_script, human checklist, take manifest, and session manifest.",
        "- canon evidence comes from canon files and validators, not from recording_batches.md.",
        "- Future recording_items_enriched.jsonl can bridge script rows to Dapu Event IR, but should not be created before real archive/segment provenance is stable.",
        "",
        "## 13. Real Sample QC Recommendation",
        "",
        "- Check WAV exists and is non-empty.",
        "- Check sample_rate, bit_depth, channel count, and file format consistency.",
        "- Check clipping and excessive silence head/tail.",
        "- Require attack_marker_ms for promoted samples.",
        "- Record release_tail_ms and ensure decay is long enough.",
        "- Check duration range by sample_type.",
        "- Ensure context sample covers the full event_range.",
        "- Track repeated takes separately.",
        "- Use quality_status values: good, usable, needs_review, reject.",
        "",
        "## 14. Render With Real Samples Recommendation",
        "",
        "- render_audio.py currently works against sample_assets and dummy WAV assumptions; it can continue after real rows exist if sample format matches.",
        "- Add source_type preference so real_recording is preferred while dummy remains fallback.",
        "- Rotate among multiple good takes per gesture to avoid immediate repetition.",
        "- Include realization_variant and realization_pre_action in selection.",
        "- Context samples should be excluded from ordinary render until policy specifies when to use them.",
        "- Add a sample_set selector before replacing dummy-first behavior.",
        "",
        "## 15. Do Not Immediately Execute",
        "",
        *bullet(gap_report["do_not_create_now"]),
        "",
        "## 16. Next Phase 1B Order",
        "",
        "1. Phase 1B-1: decide session manifest and recording format.",
        "2. Phase 1B-2: archive raw audio and create take manifest.",
        "3. Phase 1B-3: manually or semi-automatically split a small pilot batch.",
        "4. Phase 1B-4: QC segments, mark attack/tail/quality.",
        "5. Phase 1B-5: promote good segments into real sample_assets and sample set.",
        "6. Phase 1B-6: render with real samples and review by listening.",
        "",
    ]
    REPORT_MD.write_text("\n".join(section_lines), encoding="utf-8")


def write_next_steps() -> None:
    lines = [
        "# Recording Ingest Next Steps",
        "",
        "Scope: Phase 1B route after the read-only readiness audit. Do not treat this file as recording ingest data.",
        "",
        "## Phase 1B-1: Recording Session Metadata",
        "",
        "Goal: establish session_manifest template and lock the recording mode before audio enters the repository.",
        "",
        "- Inputs: recording_script_human.csv, recording_batches.md, qinist/qin/tuning IDs, chosen recorder settings.",
        "- Outputs: approved session_manifest template and agreed file naming policy.",
        "- Modifies data: yes, future manifest only; no audio slicing.",
        "- Human confirmation: required for recording_mode, sample_rate, bit_depth, channel count, room, qin, and tuning.",
        "",
        "## Phase 1B-2: Raw Audio Archive",
        "",
        "Goal: put true recordings into raw audio storage while preserving originals.",
        "",
        "- Inputs: raw WAV files, session_manifest, 71-task checklist.",
        "- Outputs: raw/ originals, normalized/ copies if needed, take_manifest.csv.",
        "- Modifies data: yes, raw archive and take manifest; no sample_assets rows.",
        "- Human confirmation: required for take boundary policy, slate policy, retake naming, and selected recording session ID.",
        "",
        "## Phase 1B-3: Manual / Semi-auto Split",
        "",
        "Goal: cut source audio into recording_segments using take_manifest and recording_script references.",
        "",
        "- Inputs: raw or normalized WAV, take_manifest, recording_script.csv, optional Audacity/Reaper timestamp export.",
        "- Outputs: candidate segment files and recording_segments rows.",
        "- Modifies data: yes, future segment files/table only after schema patch.",
        "- Human confirmation: required for context event_range and ambiguous take boundaries.",
        "",
        "## Phase 1B-4: Segment QC",
        "",
        "Goal: verify each segment before it becomes a renderable sample.",
        "",
        "- Inputs: recording_segments, segment audio, session manifest.",
        "- Outputs: qc_status, attack_marker_ms, release_tail_ms, quality_status, selected_for_sample decisions.",
        "- Modifies data: yes, segment QC metadata.",
        "- Human confirmation: required for borderline tone quality, clipping, noisy room, wrong attack, and reshoot decisions.",
        "",
        "## Phase 1B-5: Promote to Sample Assets",
        "",
        "Goal: generate real sample_assets rows from good segments while keeping dummy fallback.",
        "",
        "- Inputs: good/usable recording_segments, sample selection policy, existing sample_assets schema.",
        "- Outputs: real_recording sample_assets rows and a selected sample set.",
        "- Modifies data: yes, sample_assets and possibly sample set metadata after a V1 minimal patch.",
        "- Human confirmation: required for active sample set and multiple-take choice.",
        "",
        "## Phase 1B-6: Render With Real Samples",
        "",
        "Goal: render the first real-sample Sanman Xianwengcao candidate.",
        "",
        "- Inputs: active real sample set, dummy fallback, rhythm candidates, render_audio.py selection rules.",
        "- Outputs: first real-sample render and listening review notes.",
        "- Modifies data: yes, render outputs only.",
        "- Human confirmation: required for whether context samples participate and whether dummy fallback remains audible.",
        "",
        "Recommended first pilot: choose a small subset that includes one straight, one chuo, one zhu, and one context transition before processing all 71 tasks.",
        "",
    ]
    REPORT_NEXT.write_text("\n".join(lines), encoding="utf-8")


def write_decisions() -> None:
    decisions = [
        "Recording mode: one continuous/batch-level take or 71 separate files?",
        "Should every task begin with a spoken or tapped identifier?",
        "Should spoken identifiers remain in raw files or be removed only in normalized copies?",
        "Should every take preserve 2-3 seconds of tail decay?",
        "Capture format: 44.1 kHz or 48 kHz, 16-bit or 24-bit?",
        "Channel count: mono or stereo?",
        "File format: WAV only or another archival format?",
        "Use the same qin QIN_A for all takes?",
        "Fix tuning to ZHENG_DIAO for the entire session?",
        "Allow multiple takes per task?",
        "Retake naming: suffix by retake number, quality, or both?",
        "Recording order: atomic first then context, or grouped by the existing batches?",
        "Start with manual splitting rather than automatic slicing?",
        "Record a room-noise sample?",
        "Record tuning reference tones before and after the session?",
        "Should context takes be promoted into sample_assets immediately or kept as training/reference evidence?",
        "Which sample set should render_audio prefer after real samples exist?",
    ]
    lines = [
        "# Recording Ingest Decisions Needed",
        "",
        "These are the user/recording-team decisions needed before real recording or before cutting the first pilot batch.",
        "",
        *[f"{idx}. {item}" for idx, item in enumerate(decisions, start=1)],
        "",
    ]
    REPORT_DECISIONS.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    files = checked_files()
    summary = summarize_rows()
    gap_report = build_gap_report(summary, files)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    write_readiness_md(summary, gap_report)
    REPORT_JSON.write_text(json.dumps(gap_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_next_steps()
    write_decisions()

    print(f"Recording ingest readiness status: {gap_report['readiness_status']}")
    print(f"Wrote {rel(REPORT_MD)}")
    print(f"Wrote {rel(REPORT_JSON)}")
    print(f"Wrote {rel(REPORT_NEXT)}")
    print(f"Wrote {rel(REPORT_DECISIONS)}")
    return 0 if gap_report["readiness_status"] in {"pass", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
