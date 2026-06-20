from __future__ import annotations

import csv
import json
import math
import os
import shutil
import wave
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import REVIEW_OUTPUT_ROOT, TOOL_DIR
from app.schemas import (
    R2DraftPayload,
    R2DraftResponse,
    R2ExportRequest,
    R2ListeningReview,
    R2PhraseDefinition,
    R2PhraseMarker,
    R2Piece,
    R2RenderPhraseAlignment,
    R2RenderRevisionLog,
    R2RenderSet,
    R2RenderVersion,
    R2Section,
    R2Session,
)


SAFETY = {
    "review_only": True,
    "production_grade": False,
    "not_render_executed": True,
    "not_sample_assets": True,
    "not_ml_training_data": True,
}

RENDER_SET_ID = "R2A_MOCK_XWC_BAIYA_001"
REPO_ROOT = TOOL_DIR.parents[1]

PIECES = [
    R2Piece(piece_id="XWC", piece_title="仙翁操", active_mvp=True, mock_only=False),
    R2Piece(piece_id="JK", piece_title="酒狂", mock_only=True),
    R2Piece(piece_id="OLWJ", piece_title="鸥鹭忘机", mock_only=True),
    R2Piece(piece_id="MHSN", piece_title="梅花三弄", mock_only=True),
]

SESSIONS = [
    R2Session(recording_session_id="RS_XWC_002_BAIYA_PILOT", label="白牙 pilot / current session", current_project_session=True, mock_only=False),
    R2Session(recording_session_id="DEMO_SESSION_001", label="UI mock only", mock_only=True),
    R2Session(recording_session_id="DEMO_SESSION_002", label="UI mock only", mock_only=True),
]

RENDER_SET = R2RenderSet(
    render_set_id=RENDER_SET_ID,
    project_id="CG_VARW",
    recording_session_id="RS_XWC_002_BAIYA_PILOT",
    piece_id="XWC",
    piece_title="仙翁操",
    qinist_id="QINIST_002",
    created_at="2026-06-15T00:00:00+08:00",
    **SAFETY,
)

SECTIONS = [
    R2Section(section_id="SECTION_01", section_label="起首", event_range="XWC_P01_N01_to_XWC_P02_N04", phrase_ids=["PHRASE_01", "PHRASE_02"]),
    R2Section(section_id="SECTION_02", section_label="承接", event_range="XWC_P03_N01_to_XWC_P04_N04", phrase_ids=["PHRASE_03", "PHRASE_04"]),
    R2Section(section_id="SECTION_03", section_label="转合", event_range="XWC_P05_N01_to_XWC_P06_N03", phrase_ids=["PHRASE_05"]),
]

PHRASES = [
    R2PhraseDefinition(phrase_id="PHRASE_01", section_id="SECTION_01", phrase_index=1, phrase_label="初起一息", event_range="XWC_P01_N01_to_N03", start_event_id="XWC_P01_N01", end_event_id="XWC_P01_N03"),
    R2PhraseDefinition(phrase_id="PHRASE_02", section_id="SECTION_01", phrase_index=2, phrase_label="虚收", event_range="XWC_P02_N01_to_N04", start_event_id="XWC_P02_N01", end_event_id="XWC_P02_N04"),
    R2PhraseDefinition(phrase_id="PHRASE_03", section_id="SECTION_02", phrase_index=3, phrase_label="承接短句", event_range="XWC_P03_N02_to_N04", start_event_id="XWC_P03_N02", end_event_id="XWC_P03_N04"),
    R2PhraseDefinition(phrase_id="PHRASE_04", section_id="SECTION_02", phrase_index=4, phrase_label="回身", event_range="XWC_P04_N01_to_N04", start_event_id="XWC_P04_N01", end_event_id="XWC_P04_N04"),
    R2PhraseDefinition(phrase_id="PHRASE_05", section_id="SECTION_03", phrase_index=5, phrase_label="收合", event_range="XWC_P05_N01_to_XWC_P06_N03", start_event_id="XWC_P05_N01", end_event_id="XWC_P06_N03"),
]


def list_projects() -> list[dict[str, Any]]:
    return [{"project_id": "CG_VARW", "project_name": "Cyber Guqin v1.0", **SAFETY}]


def list_pieces() -> list[R2Piece]:
    intake = load_intake_index()
    if intake:
        return [R2Piece(piece_id=intake["piece_id"], piece_title=intake["piece_title"], active_mvp=True, mock_only=False)]
    return PIECES


def list_sessions() -> list[R2Session]:
    intake = load_intake_index()
    if intake:
        return [
            R2Session(
                recording_session_id=intake["recording_session_id"],
                label=f"{intake.get('qinist_name', intake['qinist_id'])} / render set intake",
                current_project_session=True,
                mock_only=False,
            )
        ]
    return SESSIONS


def list_render_sets() -> list[R2RenderSet]:
    intake = load_intake_index()
    if intake:
        return [render_set_from_intake(intake)]
    return [RENDER_SET]


def get_render_set(render_set_id: str) -> R2RenderSet:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        return render_set_from_intake(intake)
    _require_render_set(render_set_id)
    return RENDER_SET


def list_versions(render_set_id: str) -> list[R2RenderVersion]:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        return versions_from_intake(intake)
    _require_render_set(render_set_id)
    specs = [
        ("A_LITERAL", "A", "直译谱面版", "Literal Dapu", "literal_dapu", 108.4),
        ("B_PHRASE", "B", "句法呼吸版", "Phrase Dapu", "phrase_dapu", 106.3),
        ("C_QINIST_STYLE", "C", "琴人风格版", "Qinist Style Dapu", "qinist_style_dapu", 111.1),
        ("D_TEACHING", "D", "教学诊断版", "Teaching Diagnostic Dapu", "teaching_diagnostic_dapu", 113.7),
        ("E_REVIEWED", "E", "听评修订版", "Reviewed Dapu", "reviewed_dapu", 107.8),
    ]
    return [
        R2RenderVersion(
            render_set_id=render_set_id,
            version_id=version_id,
            version_code=code,  # type: ignore[arg-type]
            version_label_zh=label_zh,
            version_label_en=label_en,
            version_role=role,  # type: ignore[arg-type]
            audio_path=f"mock://r2/{version_id}",
            duration_s=duration,
            waveform_preview=mock_waveform(120, index),
            mock_render=True,
            **SAFETY,
        )
        for index, (version_id, code, label_zh, label_en, role, duration) in enumerate(specs)
    ]


def list_phrases(render_set_id: str) -> dict[str, Any]:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        return phrases_from_intake(intake)
    _require_render_set(render_set_id)
    return {"sections": SECTIONS, "phrases": PHRASES, **SAFETY}


def list_alignments(render_set_id: str) -> list[R2RenderPhraseAlignment]:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        return alignments_from_intake(intake)
    _require_render_set(render_set_id)
    starts = {
        "PHRASE_01": [0.4, 0.2, 0.6, 0.3, 0.4],
        "PHRASE_02": [16.8, 16.4, 17.2, 16.9, 16.6],
        "PHRASE_03": [38.42, 39.08, 37.86, 40.12, 38.74],
        "PHRASE_04": [63.52, 62.96, 65.04, 66.2, 63.4],
        "PHRASE_05": [83.1, 81.94, 86.2, 88.12, 82.66],
    }
    lengths = {
        "PHRASE_01": [12.9, 13.4, 13.1, 14.2, 13.2],
        "PHRASE_02": [17.3, 17.9, 18.1, 19.2, 17.5],
        "PHRASE_03": [20.36, 21.82, 22.18, 23.46, 21.16],
        "PHRASE_04": [16.92, 17.84, 18.96, 19.04, 17.62],
        "PHRASE_05": [19.6, 20.4, 21.7, 22.5, 20.1],
    }
    rows: list[R2RenderPhraseAlignment] = []
    for phrase in PHRASES:
        for version_index, version in enumerate(list_versions(render_set_id)):
            start = starts[phrase.phrase_id][version_index]
            length = lengths[phrase.phrase_id][version_index]
            rows.append(
                R2RenderPhraseAlignment(
                    render_set_id=render_set_id,
                    version_id=version.version_id,
                    phrase_id=phrase.phrase_id,
                    section_id=phrase.section_id,
                    event_range=phrase.event_range,
                    start_s=start,
                    end_s=round(start + length, 3),
                    breath_points_s=[round(start + length * (0.42 if version.version_code == "D" else 0.38), 3)],
                    cadence_point_s=round(start + length * 0.82, 3),
                    boundary_source="mock",
                    boundary_confidence="medium" if version.version_code == "D" else "high",
                    review_status="unclear" if phrase.phrase_id == "PHRASE_03" and version.version_code == "D" else "candidate",
                    reviewer="mock_reviewer",
                    reviewed_at="2026-06-15T00:00:00+08:00",
                    notes="R2A phrase-aligned mock boundary; not rendered audio.",
                )
            )
    return rows


def event_timeline(render_set_id: str) -> dict[str, Any]:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        phrases = phrases_from_intake(intake)["phrases"]
        return {
            "render_set_id": render_set_id,
            "events": [
                {"event_id": phrase.start_event_id, "phrase_id": phrase.phrase_id, "role": "start"}
                for phrase in phrases
            ]
            + [{"event_id": phrase.end_event_id, "phrase_id": phrase.phrase_id, "role": "end"} for phrase in phrases],
            **SAFETY,
        }
    _require_render_set(render_set_id)
    return {
        "render_set_id": render_set_id,
        "events": [
            {"event_id": phrase.start_event_id, "phrase_id": phrase.phrase_id, "role": "start"}
            for phrase in PHRASES
        ]
        + [{"event_id": phrase.end_event_id, "phrase_id": phrase.phrase_id, "role": "end"} for phrase in PHRASES],
        **SAFETY,
    }


def load_draft(render_set_id: str) -> R2DraftResponse:
    _require_render_set(render_set_id)
    path = draft_path(render_set_id)
    if not path.exists():
        return R2DraftResponse(render_set_id=render_set_id, exists=False, **SAFETY)
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    draft = R2DraftPayload(**data)
    return R2DraftResponse(render_set_id=render_set_id, exists=True, saved_at=draft.saved_at, draft=draft, **SAFETY)


def save_draft(payload: R2DraftPayload) -> dict[str, Any]:
    _require_render_set(payload.render_set_id)
    path = draft_path(payload.render_set_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = payload.model_dump()
    data.update(SAFETY)
    if not data.get("saved_at"):
        data["saved_at"] = now()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {"path": str(path), "saved": True}


def load_project_review_draft_latest(render_set_id: str) -> dict[str, Any]:
    _require_render_set_or_intake(render_set_id)
    path = r2_review_draft_latest_dir() / "r2_review_state.latest.json"
    if not path.exists():
        return {
            "render_set_id": render_set_id,
            "has_draft": False,
            "draft_source": "none",
            "canonical_state_path": str(path),
            **SAFETY,
        }
    with path.open("r", encoding="utf-8") as handle:
        draft = json.load(handle)
    manifest_path = path.parent / "r2_review_state_manifest.json"
    manifest = read_json_if_exists(manifest_path)
    counts = canonical_state_counts(draft)
    return {
        "render_set_id": render_set_id,
        "has_draft": True,
        "draft_source": "engineering_dir_latest",
        "canonical_state_path": str(path),
        "path": str(path),
        "latest_dir": str(path.parent),
        "saved_at": draft.get("saved_at") or draft.get("provenance", {}).get("restored_at") or manifest.get("saved_at", ""),
        "review_count": counts["review_count"],
        "phrase_count": counts["phrase_count"],
        "preferred_version_count": counts["preferred_version_count"],
        "suggested_revision_count": counts["suggested_revision_count"],
        "manifest": manifest,
        "draft": draft,
        **SAFETY,
    }


def save_project_review_draft(render_set_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    _require_render_set_or_intake(render_set_id)
    saved_at = now()
    state = canonicalize_project_review_state(dict(payload), archived_at=saved_at)
    state["render_set_id"] = render_set_id
    state["saved_at"] = saved_at
    state["review_status"] = state.get("review_status") or "draft"
    state.update(SAFETY)
    state["gpt_review_pending"] = True
    state["e_revision_plan_generated"] = False
    state["e_generated"] = False
    apply_f_pending_flags(state)
    counts = canonical_state_counts(state)
    state.update(counts)
    state.setdefault("provenance", {})
    state["provenance"].update({
        "saved_from_frontend": True,
        "saved_at": saved_at,
        "canonical_source": "r2_review_state.latest.json",
        "current_page_load_source": "engineering_dir_latest",
        "no_downloads_policy": True,
    })

    latest_dir = r2_review_draft_latest_dir()
    archive_dir = r2_review_draft_archive_dir(saved_at)
    latest_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)

    state_path = latest_dir / "r2_review_state.latest.json"
    write_json(state_path, state)
    export_tables = export_tables_from_canonical_state(render_set_id, state)
    files = write_export_tables(latest_dir, export_tables)
    manifest = write_review_state_manifest(latest_dir, state, files, archive_dir)
    copy_latest_to_archive(latest_dir, archive_dir)
    return {
        "path": str(state_path),
        "state_path": str(state_path),
        "latest_dir": str(latest_dir),
        "archive_dir": str(archive_dir),
        "manifest_path": str(manifest),
        "files": [str(path) for path in files],
        "review_count": state["review_count"],
        "phrase_count": state["phrase_count"],
        "preferred_version_count": state["preferred_version_count"],
        "suggested_revision_count": state["suggested_revision_count"],
        **SAFETY,
    }


def export_project_review_draft_csv(render_set_id: str) -> dict[str, Any]:
    _require_render_set_or_intake(render_set_id)
    exported_at = now()
    latest_dir = r2_review_draft_latest_dir()
    state_path = latest_dir / "r2_review_state.latest.json"
    if not state_path.exists():
        raise ValueError(f"R2 latest draft not found: {state_path}")
    with state_path.open("r", encoding="utf-8") as handle:
        state = json.load(handle)
    state = canonicalize_project_review_state(state, archived_at=exported_at)
    state["render_set_id"] = render_set_id
    state["saved_at"] = state.get("saved_at") or exported_at
    state.update(SAFETY)
    state["gpt_review_pending"] = True
    state["e_revision_plan_generated"] = False
    state["e_generated"] = False
    apply_f_pending_flags(state)
    state["provenance"] = state.get("provenance", {}) if isinstance(state.get("provenance"), dict) else {}
    state["provenance"].update({
        "exported_csv_to_project_dir": True,
        "exported_at": exported_at,
        "canonical_source": "r2_review_state.latest.json",
        "current_page_load_source": "engineering_dir_latest",
        "no_downloads_policy": True,
    })
    state.update(canonical_state_counts(state))
    latest_dir.mkdir(parents=True, exist_ok=True)
    write_json(state_path, state)
    export_tables = export_tables_from_canonical_state(render_set_id, state)
    files = write_export_tables(latest_dir, export_tables)
    manifest = write_review_state_manifest(latest_dir, state, files, latest_dir)
    return {
        "path": str(latest_dir),
        "state_path": str(state_path),
        "latest_dir": str(latest_dir),
        "manifest_path": str(manifest),
        "files": [str(path) for path in files],
        "review_count": state["review_count"],
        "phrase_count": state["phrase_count"],
        "preferred_version_count": state["preferred_version_count"],
        "suggested_revision_count": state["suggested_revision_count"],
        "issue_count": state["issue_count"],
        **SAFETY,
    }


def restore_project_review_draft_from_export_dir(render_set_id: str, export_dir: str | Path | None = None) -> dict[str, Any]:
    _require_render_set_or_intake(render_set_id)
    source_dir = Path(export_dir).expanduser().resolve() if export_dir else default_restore_export_dir()
    export_files = load_export_files(source_dir)
    missing = [name for name in expected_export_files() if name not in export_files]
    if "listening_review.csv" not in export_files:
        raise ValueError(f"listening_review.csv not found in export dir: {source_dir}")

    review_rows = read_csv_text(export_files["listening_review.csv"])
    preferred_rows = read_csv_text(export_files.get("preferred_version_summary.csv", ""))
    issue_rows = read_csv_text(export_files.get("issue_list.csv", ""))
    structure_rows = read_yaml_table_rows(export_files.get("phrase_structure_review.yaml", ""))
    alignment_rows_from_export = read_csv_text(export_files.get("render_phrase_alignment.csv", ""))
    boundary_rows_from_export = read_csv_text(export_files.get("phrase_boundary_decision.csv", ""))
    revision_rows_from_export = read_yaml_table_rows(export_files.get("render_revision_log.yaml", ""))

    warnings: list[str] = []
    if missing:
        warnings.append(f"missing export files: {', '.join(missing)}")
    all_alignments = list_alignments(render_set_id)
    if alignment_rows_from_export and len(alignment_rows_from_export) != len(all_alignments):
        warnings.append(f"render_phrase_alignment.csv has {len(alignment_rows_from_export)} rows; current render set expects {len(all_alignments)} rows, so it was not used as alignment authority")
    if boundary_rows_from_export and len(boundary_rows_from_export) != len(all_alignments):
        warnings.append(f"phrase_boundary_decision.csv has {len(boundary_rows_from_export)} rows; current render set expects {len(all_alignments)} rows, so only explicit boundary_status values were restored")
    suggested_count = sum(1 for row in review_rows if row.get("suggested_revision", "").strip())
    if revision_rows_from_export and len(revision_rows_from_export) != suggested_count:
        warnings.append(f"render_revision_log.yaml has {len(revision_rows_from_export)} rows; listening_review.csv has {suggested_count} non-empty suggested_revision rows, so revision log was regenerated from listening reviews")

    preferred = preferred_versions_from_rows(preferred_rows, review_rows)
    boundary_status = boundary_status_from_rows(boundary_rows_from_export)
    listening_by_key = listening_reviews_from_rows(review_rows, preferred)
    active_review = review_rows[0] if review_rows else {}
    restored_at = now()
    state = {
        "render_set_id": render_set_id,
        "data_source": "api",
        "review_status": "draft",
        "active_phrase_id": active_review.get("phrase_id") or "",
        "active_version_id": active_review.get("active_version_id") or "",
        "selected_marker_id": "",
        "boundaryStatusByKey": boundary_status,
        "listeningReviewByKey": listening_by_key,
        "preferredVersionByPhrase": preferred,
        "review_count": len(review_rows),
        "phrase_count": len({row.get("phrase_id", "") for row in review_rows if row.get("phrase_id")}),
        "preferred_version_count": len([value for value in preferred.values() if value]),
        "issue_count": len(issue_rows),
        "suggested_revision_count": suggested_count,
        "gpt_review_pending": True,
        "e_revision_plan_generated": False,
        "e_generated": False,
        "f_generation_pending": True,
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_not_generated": True,
        "experimental_render": True,
        "production_grade": False,
        "provenance": {
            "restored_from_exports": True,
            "source_export_dir": str(source_dir),
            "restored_at": restored_at,
            "restore_warnings": warnings,
            "listening_review_csv_rows": len(review_rows),
            "listening_review_yaml_found": "listening_review.yaml" in export_files,
            "phrase_structure_rows": len(structure_rows),
        },
        **SAFETY,
    }
    state = canonicalize_project_review_state(state, archived_at=restored_at)
    apply_f_pending_flags(state)
    state.update(canonical_state_counts(state))
    latest_dir = r2_review_draft_latest_dir()
    archive_dir = r2_review_draft_archive_dir(restored_at)
    latest_dir.mkdir(parents=True, exist_ok=True)
    archive_dir.mkdir(parents=True, exist_ok=True)
    state_path = latest_dir / "r2_review_state.latest.json"
    write_json(state_path, state)

    tables = export_tables_from_canonical_state(render_set_id, state)
    files = write_export_tables(latest_dir, tables)
    manifest = write_review_state_manifest(latest_dir, state, files, archive_dir)
    copy_latest_to_archive(latest_dir, archive_dir)
    return {
        "path": str(latest_dir),
        "state_path": str(state_path),
        "latest_dir": str(latest_dir),
        "archive_dir": str(archive_dir),
        "manifest_path": str(manifest),
        "restored_review_count": len(review_rows),
        "phrase_count": state["phrase_count"],
        "preferred_version_count": state["preferred_version_count"],
        "suggested_revision_count": suggested_count,
        "warning_count": len(warnings),
        "restore_warnings": warnings,
        "files": [str(path) for path in files],
        **SAFETY,
    }


def save_payload(name: str, payload: dict[str, Any]) -> dict[str, Any]:
    render_set_id = str(payload.get("render_set_id", RENDER_SET_ID))
    _require_render_set(render_set_id)
    path = REVIEW_OUTPUT_ROOT / "r2" / "drafts" / f"{render_set_id}.{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload.update(SAFETY)
    payload["saved_at"] = now()
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return {"path": str(path), "saved": True}


def export_reviews(request: R2ExportRequest) -> dict[str, Any]:
    _require_render_set(request.render_set_id)
    out_dir = REVIEW_OUTPUT_ROOT / "r2" / "exports" / request.render_set_id / now_path()
    out_dir.mkdir(parents=True, exist_ok=True)
    alignments = list_alignments(request.render_set_id)
    if request.scope == "phrase" and request.phrase_id:
        alignments = [item for item in alignments if item.phrase_id == request.phrase_id]

    files = [
        write_text(out_dir / "phrase_structure_review.yaml", yaml_dump({"sections": SECTIONS, "phrases": PHRASES, **SAFETY})),
        write_csv(out_dir / "render_phrase_alignment.csv", alignment_rows(alignments)),
        write_csv(out_dir / "phrase_boundary_decision.csv", boundary_rows(alignments)),
        write_text(out_dir / "listening_review.yaml", yaml_dump({"reviews": [default_review().model_dump()], **SAFETY})),
        write_text(out_dir / "render_revision_log.yaml", yaml_dump({"revision_logs": [default_revision().model_dump()], **SAFETY})),
        write_csv(out_dir / "preferred_version_summary.csv", preferred_rows(alignments)),
        write_csv(out_dir / "issue_list.csv", issue_rows()),
    ]
    return {"path": str(out_dir), "files": [str(path) for path in files], **SAFETY}


def export_rows(render_set_id: str) -> list[dict[str, Any]]:
    _require_render_set(render_set_id)
    return [
        {"file": "phrase_structure_review.yaml", "group": "句读结构", "description": "section / phrase / marker 结构", "scope": "current piece", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "render_phrase_alignment.csv", "group": "版本对齐", "description": "A/B/C/D/E 每个 phrase 的 start/end", "scope": "all mock phrases", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "phrase_boundary_decision.csv", "group": "句读结构", "description": "句读边界决策", "scope": "current phrase", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "listening_review.yaml", "group": "听评记录", "description": "听评批注与 issue_type", "scope": "current phrase", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "render_revision_log.yaml", "group": "修订依据", "description": "后续修订依据，不生成 E/F", "scope": "review-only", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "preferred_version_summary.csv", "group": "汇总", "description": "偏好版本汇总", "scope": "all mock phrases", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
        {"file": "issue_list.csv", "group": "汇总", "description": "全曲问题清单", "scope": "all mock phrases", "actor": "mock_reviewer", "updated_at": "2026-06-15T00:00:00+08:00"},
    ]


def load_intake_index() -> dict[str, Any] | None:
    path = get_r2_intake_index_path()
    if not path or not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_r2_intake_root() -> Path | None:
    configured = os.environ.get("CG_VARW_R2_INTAKE_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    path = discover_r2_intake_index_path()
    return path.parent if path else None


def get_r2_render_root() -> Path | None:
    configured = os.environ.get("CG_VARW_R2_RENDER_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    intake_root = get_r2_intake_root()
    if intake_root and intake_root.name == "r2_review_intake":
        return intake_root.parent.resolve()
    return None


def get_r2_intake_index_path() -> Path | None:
    intake_root = get_r2_intake_root()
    if intake_root:
        return intake_root / "r2_render_set_index.json"
    return discover_r2_intake_index_path()


def get_r2_alignment_seed_path() -> Path | None:
    intake_root = get_r2_intake_root()
    if not intake_root:
        return None
    playback_safe_seed = intake_root / "r2_phrase_alignment_seed.playback_safe.csv"
    if playback_safe_seed.exists():
        return playback_safe_seed
    score_lock_seed = intake_root / "r2_phrase_alignment_seed.from_score_phrase_lock.csv"
    if score_lock_seed.exists():
        return score_lock_seed
    return intake_root / "r2_phrase_alignment_seed.csv"


def get_r2_phrase_lock_path() -> Path | None:
    intake_root = get_r2_intake_root()
    if not intake_root:
        return None
    lock_dir = intake_root / "phrase_structure_lock"
    matches = sorted(lock_dir.glob("*_PHRASE_STRUCTURE_LOCK_DRAFT.csv"))
    return matches[0] if matches else None


def e_reviewed_dir() -> Path | None:
    render_root = get_r2_render_root()
    candidates = []
    if render_root:
        candidates.append(render_root / "E_REVIEWED")
    intake_root = get_r2_intake_root()
    if intake_root:
        candidates.append(intake_root.parent / "E_REVIEWED")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else None


def e_reviewed_audio_path() -> Path | None:
    e_dir = e_reviewed_dir()
    return e_dir / "XWC_BAIYA_E_REVIEWED.wav" if e_dir else None


def e_reviewed_alignment_path() -> Path | None:
    e_dir = e_reviewed_dir()
    return e_dir / "render_event_alignment.E_REVIEWED.csv" if e_dir else None


def f_final_reviewed_dir() -> Path | None:
    render_root = get_r2_render_root()
    if render_root:
        return render_root / "F_FINAL_REVIEWED"
    candidates = []
    intake_root = get_r2_intake_root()
    if intake_root:
        candidates.append(intake_root.parent / "F_FINAL_REVIEWED")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if candidates else None


def f_final_reviewed_audio_path() -> Path | None:
    f_dir = f_final_reviewed_dir()
    return f_dir / "XWC_BAIYA_F_FINAL_REVIEWED.wav" if f_dir else None


def f_final_reviewed_alignment_path() -> Path | None:
    f_dir = f_final_reviewed_dir()
    return f_dir / "render_event_alignment.F_FINAL_REVIEWED.csv" if f_dir else None


def wav_duration_s(path: Path) -> float:
    try:
        with wave.open(str(path), "rb") as handle:
            return round(handle.getnframes() / float(handle.getframerate()), 6)
    except (wave.Error, OSError, ZeroDivisionError):
        return 0.0


def discover_r2_intake_index_path() -> Path | None:
    matches = sorted(REPO_ROOT.glob("04_outputs/*/*/abcd_experimental_render/r2_review_intake/r2_render_set_index.json"))
    return matches[0] if matches else None


def render_set_from_intake(intake: dict[str, Any]) -> R2RenderSet:
    return R2RenderSet(
        render_set_id=intake["render_set_id"],
        project_id="CG_VARW",
        recording_session_id=intake["recording_session_id"],
        piece_id=intake["piece_id"],
        piece_title=intake["piece_title"],
        qinist_id=intake["qinist_id"],
        render_stage="experimental_render",
        created_at=intake.get("created_at", now()),
        **SAFETY,
    )


def versions_from_intake(intake: dict[str, Any]) -> list[R2RenderVersion]:
    role_map = {
        "A_LITERAL": ("A", "直译谱面版", "Literal Dapu", "literal_dapu"),
        "B_PHRASE": ("B", "句法呼吸版", "Phrase Dapu", "phrase_dapu"),
        "C_QINIST_STYLE": ("C", "琴人风格版", "Qinist Style Dapu", "qinist_style_dapu"),
        "D_TEACHING_DIAGNOSTIC": ("D", "教学诊断版", "Teaching Diagnostic Dapu", "teaching_diagnostic_dapu"),
    }
    versions: list[R2RenderVersion] = []
    for index, item in enumerate(intake.get("versions", [])):
        version_id = item["version_id"]
        if version_id not in role_map:
            continue
        code, label_zh, label_en, role = role_map[version_id]
        versions.append(
            R2RenderVersion(
                render_set_id=intake["render_set_id"],
                version_id=version_id,
                version_code=code,  # type: ignore[arg-type]
                version_label_zh=label_zh,
                version_label_en=label_en,
                version_role=role,  # type: ignore[arg-type]
                audio_path=item["wav_path"],
                duration_s=float(item.get("duration_s") or 0),
                waveform_preview=mock_waveform(120, index),
                mock_render=False,
                status="available",
                playable=True,
                alignment_available=True,
                source="abcd_experimental_render",
                generation_allowed=False,
                **SAFETY,
            )
        )
    e_audio_path = e_reviewed_audio_path()
    e_alignment_path = e_reviewed_alignment_path()
    if e_audio_path and e_audio_path.exists():
        versions.append(
            R2RenderVersion(
                render_set_id=intake["render_set_id"],
                version_id="E_REVIEWED",
                version_code="E",
                version_label_zh="听评修订版",
                version_label_en="Reviewed Dapu",
                version_role="reviewed_dapu",
                audio_path=str(e_audio_path),
                duration_s=wav_duration_s(e_audio_path),
                waveform_preview=mock_waveform(120, len(versions)),
                mock_render=False,
                status="review_ready",
                playable=True,
                alignment_available=bool(e_alignment_path and e_alignment_path.exists()),
                source="e_reviewed_generation",
                generation_allowed=False,
                **SAFETY,
            )
        )
    f_audio_path = f_final_reviewed_audio_path()
    f_alignment_path = f_final_reviewed_alignment_path()
    if f_audio_path and f_audio_path.exists():
        versions.append(
            R2RenderVersion(
                render_set_id=intake["render_set_id"],
                version_id="F_FINAL_REVIEWED",
                version_code="F",
                version_label_zh="F_FINAL_REVIEWED（最终听评收束版）",
                version_label_en="Final Reviewed",
                version_role="final_reviewed_dapu",
                audio_path=str(f_audio_path),
                duration_s=wav_duration_s(f_audio_path),
                waveform_preview=mock_waveform(120, len(versions)),
                mock_render=False,
                status="final_ready",
                playable=True,
                alignment_available=bool(f_alignment_path and f_alignment_path.exists()),
                source="f_final_reviewed_generation",
                generation_allowed=False,
                **SAFETY,
            )
        )
    else:
        versions.append(
            R2RenderVersion(
                render_set_id=intake["render_set_id"],
                version_id="F_FINAL_REVIEWED",
                version_code="F",
                version_label_zh="F_FINAL_REVIEWED（待 E 听评后生成）",
                version_label_en="Final Reviewed Pending",
                version_role="final_reviewed_dapu",
                audio_path="",
                duration_s=0.0,
                waveform_preview=[],
                mock_render=False,
                status="pending",
                playable=False,
                alignment_available=False,
                source="future_from_e_review",
                generation_allowed=False,
                disabled_reason="F_FINAL_REVIEWED 尚未生成，请先完成 E_REVIEWED 听评。",
                **SAFETY,
            )
        )
    return versions


def resolve_version_audio_path(render_set_id: str, version_id: str) -> Path:
    intake = load_intake_index()
    if not intake or render_set_id != intake["render_set_id"]:
        raise ValueError(f"real R2 audio is not available for render_set_id: {render_set_id}")
    for item in intake.get("versions", []):
        if item.get("version_id") == version_id:
            path = resolve_render_path(str(item["wav_path"]))
            if not path.exists() or not path.is_file():
                raise ValueError(f"R2 version audio not found: {version_id}")
            allowed_root = (get_r2_render_root() or REPO_ROOT).resolve()
            if path != allowed_root and allowed_root not in path.parents:
                raise ValueError(f"R2 version audio outside repository: {version_id}")
            return path
    if version_id == "E_REVIEWED":
        path = e_reviewed_audio_path()
        if not path or not path.exists() or not path.is_file():
            raise ValueError("E_REVIEWED audio not found")
        return path
    if version_id == "F_FINAL_REVIEWED":
        path = f_final_reviewed_audio_path()
        if not path or not path.exists() or not path.is_file():
            raise ValueError("F_FINAL_REVIEWED 尚未生成，请先完成 E_REVIEWED 听评。")
        return path
    raise ValueError(f"unknown R2 version_id: {version_id}")


def resolve_render_path(value: str) -> Path:
    raw = Path(value).expanduser()
    candidates = [raw] if raw.is_absolute() else []
    render_root = get_r2_render_root()
    if render_root and not raw.is_absolute():
        candidates.append(render_root / raw)
        candidates.append(render_root / raw.name)
    if not raw.is_absolute():
        candidates.append(REPO_ROOT / raw)
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved
    return (candidates[-1] if candidates else raw).resolve()


def phrases_from_intake(intake: dict[str, Any]) -> dict[str, Any]:
    phrase_defs = intake.get("phrases", [])
    lock_rows = load_phrase_lock_rows()
    phrases = [
        R2PhraseDefinition(
            phrase_id=item["phrase_id"],
            section_id=item["section_id"],
            phrase_index=int(lock_rows.get(item["phrase_id"], {}).get("phrase_order") or index),
            phrase_label=lock_rows.get(item["phrase_id"], {}).get("score_phrase_label") or item["phrase_id"],
            event_range=item["event_range"],
            start_event_id=item["start_event_id"],
            end_event_id=item["end_event_id"],
            phrase_order=int(lock_rows.get(item["phrase_id"], {}).get("phrase_order") or index),
            event_count=parse_optional_int(lock_rows.get(item["phrase_id"], {}).get("event_count")),
            event_ids=lock_rows.get(item["phrase_id"], {}).get("event_ids") or "",
            gesture_ids=lock_rows.get(item["phrase_id"], {}).get("gesture_ids") or "",
            normalized_names=lock_rows.get(item["phrase_id"], {}).get("normalized_names") or "",
            gesture_summary=lock_rows.get(item["phrase_id"], {}).get("normalized_names") or lock_rows.get(item["phrase_id"], {}).get("gesture_ids") or "",
            lock_status=lock_rows.get(item["phrase_id"], {}).get("lock_status") or "",
        )
        for index, item in enumerate(phrase_defs, start=1)
    ]
    by_section: dict[str, list[R2PhraseDefinition]] = {}
    for phrase in phrases:
        by_section.setdefault(phrase.section_id, []).append(phrase)
    sections = [
        R2Section(
            section_id=section_id,
            section_label=section_id,
            event_range=f"{items[0].start_event_id}_to_{items[-1].end_event_id}",
            phrase_ids=[item.phrase_id for item in items],
        )
        for section_id, items in by_section.items()
    ]
    return {"sections": sections, "phrases": phrases, **SAFETY}


def alignments_from_intake(intake: dict[str, Any]) -> list[R2RenderPhraseAlignment]:
    path = get_r2_alignment_seed_path()
    if not path or not path.exists():
        return []
    rows: list[R2RenderPhraseAlignment] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for item in csv.DictReader(handle):
            start_s = float(item["phrase_start_s"])
            end_s = float(item["phrase_end_s"])
            play_start_s = parse_optional_float(item.get("phrase_play_start_s"))
            play_end_s = parse_optional_float(item.get("phrase_play_end_s"))
            rows.append(
                R2RenderPhraseAlignment(
                    render_set_id=intake["render_set_id"],
                    version_id=item["version_id"],
                    phrase_id=item["phrase_id"],
                    section_id=item["section_id"],
                    event_range=item["event_range"],
                    start_s=start_s,
                    end_s=end_s,
                    phrase_play_start_s=play_start_s,
                    phrase_play_end_s=play_end_s,
                    phrase_tail_end_s=parse_optional_float(item.get("phrase_tail_end_s")),
                    next_phrase_first_attack_s=parse_optional_float(item.get("next_phrase_first_attack_s")),
                    phrase_end_policy=item.get("phrase_end_policy", ""),
                    breath_points_s=[round((play_start_s or start_s) + ((play_end_s or end_s) - (play_start_s or start_s)) * 0.38, 3)],
                    cadence_point_s=round((play_start_s or start_s) + ((play_end_s or end_s) - (play_start_s or start_s)) * 0.82, 3),
                    boundary_source="imported",
                    boundary_confidence="low" if "provisional" in item.get("review_status", "") else "medium",
                    review_status="candidate",
                    reviewer=None,
                    reviewed_at=None,
                    notes="Imported from XWC ABCD r2_review_intake; review not completed.",
                )
            )
    rows.extend(e_reviewed_phrase_alignments(intake))
    rows.extend(f_final_reviewed_phrase_alignments(intake))
    return rows


def e_reviewed_phrase_alignments(intake: dict[str, Any]) -> list[R2RenderPhraseAlignment]:
    return phrase_alignments_from_render_event_alignment(
        intake,
        e_reviewed_alignment_path(),
        "E_REVIEWED",
        "Imported from E_REVIEWED render_event_alignment; F_FINAL_REVIEWED remains pending.",
    )


def f_final_reviewed_phrase_alignments(intake: dict[str, Any]) -> list[R2RenderPhraseAlignment]:
    return phrase_alignments_from_render_event_alignment(
        intake,
        f_final_reviewed_alignment_path(),
        "F_FINAL_REVIEWED",
        "Imported from F_FINAL_REVIEWED render_event_alignment; final reviewed for current iteration.",
    )


def phrase_alignments_from_render_event_alignment(
    intake: dict[str, Any],
    path: Path | None,
    version_id: str,
    notes: str,
) -> list[R2RenderPhraseAlignment]:
    if not path or not path.exists():
        return []
    phrase_rows: dict[str, list[dict[str, str]]] = {}
    phrase_order: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            phrase_id = row.get("phrase_id", "")
            if not phrase_id:
                continue
            if phrase_id not in phrase_rows:
                phrase_order.append(phrase_id)
            phrase_rows.setdefault(phrase_id, []).append(row)

    result: list[R2RenderPhraseAlignment] = []
    first_attack_by_phrase = {
        phrase_id: parse_optional_float(rows[0].get("target_attack_time_s"))
        for phrase_id, rows in phrase_rows.items()
        if rows
    }
    for index, phrase_id in enumerate(phrase_order):
        rows = phrase_rows[phrase_id]
        play_start = parse_optional_float(rows[0].get("phrase_play_start_s")) or 0.0
        play_end = max(parse_optional_float(row.get("phrase_play_end_s")) or play_start for row in rows)
        tail_end = max(play_end, max(parse_optional_float(row.get("phrase_tail_end_s")) or play_end for row in rows))
        next_phrase_id = phrase_order[index + 1] if index + 1 < len(phrase_order) else ""
        next_attack = first_attack_by_phrase.get(next_phrase_id) if next_phrase_id else None
        event_ids = [row.get("event_id", "") for row in rows if row.get("event_id")]
        result.append(
            R2RenderPhraseAlignment(
                render_set_id=intake["render_set_id"],
                version_id=version_id,
                phrase_id=phrase_id,
                section_id=rows[0].get("section_id", ""),
                event_range=f"{event_ids[0]}_to_{event_ids[-1]}" if event_ids else "",
                start_s=play_start,
                end_s=tail_end,
                phrase_play_start_s=play_start,
                phrase_play_end_s=play_end,
                phrase_tail_end_s=tail_end,
                next_phrase_first_attack_s=next_attack,
                phrase_end_policy="E_REVIEWED phrase boundary from event alignment; render_anchor based.",
                breath_points_s=[round(play_start + (play_end - play_start) * 0.38, 3)],
                cadence_point_s=round(play_start + (play_end - play_start) * 0.82, 3),
                boundary_source="imported",
                boundary_confidence="medium",
                review_status="accepted" if version_id == "F_FINAL_REVIEWED" else "candidate",
                reviewer=None,
                reviewed_at=None,
                notes=notes,
            )
        )
    return result


def load_phrase_lock_rows() -> dict[str, dict[str, str]]:
    path = get_r2_phrase_lock_path()
    if not path or not path.exists():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        return {row["phrase_id"]: row for row in csv.DictReader(handle)}


def parse_optional_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None


def parse_optional_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def mock_waveform(points: int, seed: int = 0) -> list[float]:
    return [round(max(0.08, min(1.0, abs(math.sin(index * 0.17 + seed) * 0.62 + math.sin(index * 0.047 + seed * 0.7) * 0.38))), 3) for index in range(points)]


def mock_spectrogram(points: int, seed: int = 0) -> list[float]:
    return [round(max(0.05, min(1.0, abs(math.sin(index * 0.11 + seed) * math.cos(index * 0.03 + 0.4)))), 3) for index in range(points)]


def default_review() -> R2ListeningReview:
    return R2ListeningReview(
        review_id="R2_REVIEW_PHRASE_03_B_001",
        render_set_id=RENDER_SET_ID,
        phrase_id="PHRASE_03",
        section_id="SECTION_02",
        event_range="XWC_P03_N02_to_N04",
        active_version_id="B_PHRASE",
        preferred_version_id="B_PHRASE",
        issue_type=["tail_short", "good"],
        severity="medium",
        comment="B 版句法呼吸最清楚；尾音略短，但整体保留为正向听评记录。",
        suggested_revision="后续真实修订可在 cadence 后保留更完整尾音；R2A 不生成 E 版。",
        reviewer="mock_reviewer",
        reviewed_at="2026-06-15T00:00:00+08:00",
        training_usable=False,
        **SAFETY,
    )


def default_revision() -> R2RenderRevisionLog:
    return R2RenderRevisionLog(
        revision_id="R2_REVISION_EVIDENCE_001",
        render_set_id=RENDER_SET_ID,
        from_version_id="B_PHRASE",
        to_version_id=None,
        phrase_id="PHRASE_03",
        section_id="SECTION_02",
        event_range="XWC_P03_N02_to_N04",
        change_type="tail",
        reason="Review-only evidence for a possible later revision; no E/F render is generated.",
        based_on_review_id="R2_REVIEW_PHRASE_03_B_001",
        accepted=False,
        **SAFETY,
    )


def draft_path(render_set_id: str) -> Path:
    return REVIEW_OUTPUT_ROOT / "r2" / "drafts" / f"{safe_name(render_set_id)}.r2_review_draft.json"


def alignment_rows(alignments: list[R2RenderPhraseAlignment]) -> list[dict[str, Any]]:
    return [alignment.model_dump() | SAFETY for alignment in alignments]


def boundary_rows(alignments: list[R2RenderPhraseAlignment]) -> list[dict[str, Any]]:
    return [
        {
            "render_set_id": item.render_set_id,
            "version_id": item.version_id,
            "phrase_id": item.phrase_id,
            "section_id": item.section_id,
            "event_range": item.event_range,
            "phrase_start_s": item.start_s,
            "phrase_end_s": item.end_s,
            "breath_points_s": ";".join(str(value) for value in item.breath_points_s),
            "cadence_point_s": item.cadence_point_s,
            "boundary_confidence": item.boundary_confidence,
            "review_status": item.review_status,
            **SAFETY,
        }
        for item in alignments
    ]


def preferred_rows(alignments: list[R2RenderPhraseAlignment]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    rows = []
    for item in alignments:
        if item.phrase_id in seen:
            continue
        seen.add(item.phrase_id)
        rows.append({"render_set_id": item.render_set_id, "phrase_id": item.phrase_id, "preferred_version_id": "B_PHRASE", **SAFETY})
    return rows


def issue_rows() -> list[dict[str, Any]]:
    return [{"review_id": "R2_REVIEW_PHRASE_03_B_001", "phrase_id": "PHRASE_03", "issue_type": "tail_short;good", "severity": "medium", **SAFETY}]


def r2_review_draft_root() -> Path:
    render_root = get_r2_render_root()
    if render_root:
        return render_root / "r2_review_drafts"
    return REVIEW_OUTPUT_ROOT / "r2_review_drafts"


def r2_review_draft_latest_dir() -> Path:
    return r2_review_draft_root() / "latest"


def r2_review_draft_archive_dir(saved_at: str | None = None) -> Path:
    stamp = safe_timestamp(saved_at or now())
    archive_root = r2_review_draft_root() / "archive"
    candidate = archive_root / stamp
    if not candidate.exists():
        return candidate
    for index in range(2, 100):
        candidate = archive_root / f"{stamp}_{index:02d}"
        if not candidate.exists():
            return candidate
    return archive_root / f"{stamp}_{now_path()}"


def default_restore_export_dir() -> Path:
    render_root = get_r2_render_root()
    if not render_root:
        raise ValueError("CG_VARW_R2_RENDER_ROOT is required for default R2 restore export dir")
    return render_root / "r2_review_exports" / "2026-06-20_user_review_restore_input"


def expected_export_files() -> list[str]:
    return [
        "issue_list.csv",
        "listening_review.csv",
        "listening_review.yaml",
        "phrase_boundary_decision.csv",
        "phrase_structure_review.yaml",
        "preferred_version_summary.csv",
        "render_phrase_alignment.csv",
        "render_revision_log.yaml",
    ]


def load_export_files(source_dir: Path) -> dict[str, str]:
    if not source_dir.exists():
        raise ValueError(f"R2 restore export dir not found: {source_dir}")
    files: dict[str, str] = {}
    for expected in expected_export_files():
        path = source_dir / expected
        if path.exists():
            files[expected] = path.read_text(encoding="utf-8-sig")
    if files:
        return files
    zip_matches = sorted(source_dir.glob("*.zip"))
    if not zip_matches:
        return files
    with zipfile.ZipFile(zip_matches[0]) as archive:
        for info in archive.infolist():
            basename = Path(info.filename).name
            if basename in expected_export_files():
                files[basename] = archive.read(info).decode("utf-8-sig")
    return files


def read_csv_text(text: str) -> list[dict[str, str]]:
    if not text.strip():
        return []
    return list(csv.DictReader(text.splitlines()))


def read_yaml_table_rows(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip() == "-":
            if current is not None:
                rows.append(current)
            current = {}
            continue
        if current is None or ":" not in line:
            continue
        stripped = line.strip()
        key, raw_value = stripped.split(":", 1)
        if not key or raw_value == "":
            continue
        current[key] = parse_yaml_scalar(raw_value.strip())
    if current is not None:
        rows.append(current)
    return rows


def parse_yaml_scalar(value: str) -> str:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return value
    if parsed is None:
        return ""
    if isinstance(parsed, (dict, list)):
        return json.dumps(parsed, ensure_ascii=False)
    return str(parsed)


def preferred_versions_from_rows(preferred_rows_data: list[dict[str, str]], review_rows: list[dict[str, str]]) -> dict[str, str]:
    preferred = {
        row.get("phrase_id", ""): row.get("preferred_version_id", "")
        for row in preferred_rows_data
        if row.get("phrase_id") and row.get("preferred_version_id")
    }
    for row in review_rows:
        phrase_id = row.get("phrase_id", "")
        version_id = row.get("preferred_version_id", "")
        if phrase_id and version_id and phrase_id not in preferred:
            preferred[phrase_id] = version_id
    return preferred


def boundary_status_from_rows(rows: list[dict[str, str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for row in rows:
        phrase_id = row.get("phrase_id", "")
        version_id = row.get("version_id", "")
        status = row.get("boundary_status") or row.get("review_status")
        if phrase_id and version_id and status:
            result[f"{phrase_id}:{version_id}"] = status
    return result


def listening_reviews_from_rows(rows: list[dict[str, str]], preferred: dict[str, str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        phrase_id = row.get("phrase_id", "")
        version_id = row.get("active_version_id") or row.get("version_id", "")
        if not phrase_id or not version_id:
            continue
        result[f"{phrase_id}:{version_id}"] = {
            "phrase_id": phrase_id,
            "version_id": version_id,
            "issue_type": parse_issue_type(row.get("issue_type", "")),
            "severity": row.get("severity") or "medium",
            "quick_judgement": row.get("quick_judgement") or None,
            "comment": row.get("comment", ""),
            "suggested_revision": row.get("suggested_revision", ""),
            "reviewer": row.get("reviewer") or "human",
            "reviewed_at": row.get("reviewed_at") or now(),
            "updated_at": row.get("updated_at") or row.get("reviewed_at") or now(),
            "preferred_version_id": row.get("preferred_version_id") or preferred.get(phrase_id, ""),
        }
    return result


def parse_issue_type(value: str) -> list[str]:
    text = value.strip()
    if not text or text == "[]":
        return []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed if str(item)]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in text.replace(";", ",").split(",") if item.strip()]


def restored_export_tables(
    *,
    render_set_id: str,
    review_rows: list[dict[str, str]],
    preferred_rows: list[dict[str, str]],
    issue_rows: list[dict[str, str]],
    structure_rows: list[dict[str, str]],
    alignments: list[R2RenderPhraseAlignment],
    boundary_status: dict[str, str],
    preferred: dict[str, str],
) -> dict[str, dict[str, Any]]:
    return {
        "phrase_structure_review.yaml": table_from_rows("phrase_structure_review.yaml", structure_rows or phrase_structure_rows(render_set_id)),
        "render_phrase_alignment.csv": render_phrase_alignment_table(alignments),
        "phrase_boundary_decision.csv": phrase_boundary_decision_table(alignments, boundary_status),
        "listening_review.csv": table_from_rows("listening_review.csv", ensure_draft_flags(review_rows)),
        "listening_review.yaml": table_from_rows("listening_review.yaml", ensure_draft_flags(review_rows)),
        "preferred_version_summary.csv": table_from_rows("preferred_version_summary.csv", ensure_draft_flags(preferred_rows or preferred_rows_from_map(render_set_id, preferred))),
        "issue_list.csv": table_from_rows("issue_list.csv", ensure_draft_flags(issue_rows or issue_rows_from_reviews(review_rows))),
        "render_revision_log.yaml": table_from_rows("render_revision_log.yaml", revision_rows_from_reviews(review_rows, preferred)),
    }


def canonicalize_project_review_state(state: dict[str, Any], *, archived_at: str | None = None) -> dict[str, Any]:
    next_state = dict(state)
    archived_stamp = archived_at or now()
    reviews = next_state.get("listeningReviewByKey") or next_state.get("listening_review_by_key") or {}
    normalized_reviews: dict[str, dict[str, Any]] = {}
    duplicate_groups: dict[str, list[dict[str, Any]]] = {}
    archived_reviews: list[dict[str, Any]] = []
    if isinstance(reviews, dict):
        for index, (raw_key, raw_item) in enumerate(reviews.items()):
            if not isinstance(raw_item, dict):
                continue
            item = dict(raw_item)
            key = canonical_review_key(item, str(raw_key))
            if not key:
                continue
            phrase_id, version_id = key.split(":", 1)
            item["phrase_id"] = phrase_id
            item["version_id"] = version_id
            duplicate_groups.setdefault(key, []).append({"raw_key": str(raw_key), "item": item, "index": index})
    duplicate_keys: list[str] = []
    retained_summary: list[dict[str, str]] = []
    for key, candidates in duplicate_groups.items():
        selected = max(candidates, key=lambda candidate: review_candidate_rank(candidate["item"], candidate["index"]))
        normalized_reviews[key] = selected["item"]
        phrase_id, version_id = key.split(":", 1)
        retained_summary.append({"phrase_id": phrase_id, "active_version_id": version_id, "source_key": selected["raw_key"]})
        if len(candidates) <= 1:
            continue
        duplicate_keys.append(key)
        for candidate in candidates:
            if candidate is selected:
                continue
            archived_reviews.append({
                "archived_at": archived_stamp,
                "archive_reason": "duplicate_phrase_version_retained_latest_current_review",
                "canonical_key": key,
                "source_key": candidate["raw_key"],
                "review": candidate["item"],
            })

    history = next_state.get("review_history_archived")
    if not isinstance(history, list):
        history = []
    next_state["review_history_archived"] = history + archived_reviews
    next_state["listeningReviewByKey"] = normalized_reviews
    next_state.pop("listening_review_by_key", None)
    next_state.pop("export_tables", None)
    next_state["boundaryStatusByKey"] = normalize_keyed_state(next_state.get("boundaryStatusByKey") or next_state.get("boundary_status_by_key") or {})
    next_state.pop("boundary_status_by_key", None)
    next_state["markersByKey"] = normalize_keyed_state(next_state.get("markersByKey") or next_state.get("markers_by_key") or {})
    next_state.pop("markers_by_key", None)
    next_state.update(canonical_state_counts(next_state))
    existing_report = next_state.get("canonical_dedupe_report") if isinstance(next_state.get("canonical_dedupe_report"), dict) else {}
    existing_removed = int(existing_report.get("duplicate_rows_removed_or_archived", 0) or 0)
    historical_duplicate_keys = sorted({
        str(item.get("canonical_key"))
        for item in history
        if isinstance(item, dict) and item.get("archive_reason") == "duplicate_phrase_version_retained_latest_current_review" and item.get("canonical_key")
    })
    historical_removed = len([
        item for item in history
        if isinstance(item, dict) and item.get("archive_reason") == "duplicate_phrase_version_retained_latest_current_review"
    ])
    if not archived_reviews and (existing_removed or historical_removed):
        dedupe_report = {
            **existing_report,
            "duplicate_keys_found": existing_report.get("duplicate_keys_found") or historical_duplicate_keys,
            "duplicate_rows_removed_or_archived": existing_removed or historical_removed,
            "retained_review_count": next_state["review_count"],
            "retained_suggested_revision_count": next_state["suggested_revision_count"],
            "retained_issue_count": next_state["issue_count"],
            "retained_by_phrase_version": existing_report.get("retained_by_phrase_version") or retained_summary,
            "deduped_at": existing_report.get("deduped_at") or archived_stamp,
        }
    else:
        dedupe_report = {
            "duplicate_keys_found": duplicate_keys,
            "duplicate_rows_removed_or_archived": len(archived_reviews),
            "retained_review_count": next_state["review_count"],
            "retained_suggested_revision_count": next_state["suggested_revision_count"],
            "retained_issue_count": next_state["issue_count"],
            "retained_by_phrase_version": retained_summary,
            "deduped_at": archived_stamp,
        }
    next_state["canonical_dedupe_report"] = dedupe_report
    next_state["provenance"] = next_state.get("provenance", {}) if isinstance(next_state.get("provenance"), dict) else {}
    next_state["provenance"]["canonical_dedupe_report"] = dedupe_report
    return next_state


def apply_f_pending_flags(state: dict[str, Any]) -> None:
    state["f_input_source"] = "E_REVIEWED_USER_REVIEW"
    f_completed = bool(state.get("f_generation_completed")) or (
        state.get("f_version_id") == "F_FINAL_REVIEWED" and state.get("f_generation_pending") is False
    )
    state["f_generation_pending"] = not f_completed
    state["f_not_generated"] = not f_completed
    if f_completed:
        state["f_generation_completed"] = True
        state["f_version_id"] = "F_FINAL_REVIEWED"
    provenance = state.get("provenance") if isinstance(state.get("provenance"), dict) else {}
    provenance.update({
        "f_generation_pending": state["f_generation_pending"],
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_not_generated": state["f_not_generated"],
    })
    if f_completed:
        provenance["f_generation_completed"] = True
        provenance["f_version_id"] = "F_FINAL_REVIEWED"
    state["provenance"] = provenance


def canonical_review_key(item: dict[str, Any], raw_key: str = "") -> str:
    phrase_id = str(item.get("phrase_id") or "")
    version_id = str(item.get("version_id") or item.get("active_version_id") or "")
    if (not phrase_id or not version_id) and "::" in raw_key:
        phrase_id, version_id = raw_key.split("::", 1)
    elif (not phrase_id or not version_id) and ":" in raw_key:
        phrase_id, version_id = raw_key.split(":", 1)
    return f"{phrase_id}:{version_id}" if phrase_id and version_id else ""


def normalize_keyed_state(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, Any] = {}
    for raw_key, item in value.items():
        key = str(raw_key).replace("::", ":", 1)
        result[key] = item
    return result


def review_candidate_rank(item: dict[str, Any], index: int) -> tuple[int, float, int, int]:
    return (
        explicit_current_review_score(item),
        review_timestamp_score(item),
        review_substance_score(item),
        index,
    )


def explicit_current_review_score(item: dict[str, Any]) -> int:
    phrase_id = str(item.get("phrase_id") or "")
    version_id = str(item.get("version_id") or item.get("active_version_id") or "")
    comment = str(item.get("comment") or "")
    suggested = str(item.get("suggested_revision") or "")
    text = f"{comment}\n{suggested}"
    score = 0
    if phrase_id == "XWC_P01_LOCAL_PHRASE" and version_id == "C_QINIST_STYLE" and "123——4——" in suggested:
        score += 100
    if phrase_id == "XWC_P02_LOCAL_PHRASE" and version_id == "C_QINIST_STYLE" and "12345——6——" in suggested:
        score += 100
    if phrase_id == "XWC_P09_LOCAL_PHRASE" and version_id in {"B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC"}:
        if "把带上下文的掐起和上下文连接，这样不是就有2个上下文的音了？" in text:
            score += 100
        if "带上下文的掐起不能和上下文放一起，这样不就有2个上下文的音了吗？" in text:
            score -= 100
    if phrase_id == "XWC_P10_LOCAL_PHRASE" and version_id == "A_LITERAL" and "1——234——5——6——7——" in suggested:
        score += 100
    if phrase_id == "XWC_P10_LOCAL_PHRASE" and version_id == "D_TEACHING_DIAGNOSTIC":
        if "前几个音节拍可以紧凑一点，最后3个音慢" in text or "比如1234——5——6——7这种节奏" in text:
            score -= 100
    return score


def review_timestamp_score(item: dict[str, Any]) -> float:
    for field in ("updated_at", "saved_at", "created_at", "reviewed_at"):
        value = item.get(field)
        if not value:
            continue
        try:
            text = str(value).replace("Z", "+00:00")
            return datetime.fromisoformat(text).timestamp()
        except ValueError:
            continue
    return 0.0


def review_substance_score(item: dict[str, Any]) -> int:
    score = 0
    score += min(len(str(item.get("comment") or "").strip()), 80)
    score += min(len(str(item.get("suggested_revision") or "").strip()), 80)
    issue_type = item.get("issue_type")
    if isinstance(issue_type, list):
        score += len([issue for issue in issue_type if issue]) * 20
    elif str(issue_type or "").strip():
        score += 20
    if str(item.get("quick_judgement") or "").strip():
        score += 10
    if str(item.get("preferred_version_id") or "").strip():
        score += 5
    if str(item.get("severity") or "").strip() not in {"", "low"}:
        score += 5
    return score


def export_tables_from_canonical_state(render_set_id: str, state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    state = canonicalize_project_review_state(state)
    review_rows = review_rows_from_state(render_set_id, state)
    preferred = preferred_versions_from_state(state, review_rows)
    boundary_status = boundary_status_from_state(state)
    alignments = list_alignments(render_set_id)
    flags = string_safety_flags(state)
    return {
        "phrase_structure_review.yaml": table_from_rows("phrase_structure_review.yaml", phrase_structure_rows(render_set_id, flags)),
        "render_phrase_alignment.csv": render_phrase_alignment_table(alignments, flags),
        "phrase_boundary_decision.csv": phrase_boundary_decision_table(alignments, boundary_status, flags),
        "listening_review.csv": table_from_rows("listening_review.csv", ensure_draft_flags(review_rows, flags)),
        "listening_review.yaml": table_from_rows("listening_review.yaml", ensure_draft_flags(review_rows, flags)),
        "preferred_version_summary.csv": table_from_rows("preferred_version_summary.csv", preferred_rows_from_map(render_set_id, preferred, flags)),
        "issue_list.csv": table_from_rows("issue_list.csv", issue_rows_from_reviews(review_rows, flags)),
        "render_revision_log.yaml": table_from_rows("render_revision_log.yaml", revision_rows_from_reviews(review_rows, preferred, flags)),
    }


def canonical_state_counts(state: dict[str, Any]) -> dict[str, int]:
    reviews = review_items_from_state(state)
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    return {
        "review_count": len(reviews),
        "phrase_count": len({str(item.get("phrase_id", "")) for item in reviews if item.get("phrase_id")}),
        "preferred_version_count": len([value for value in preferred.values() if value]),
        "suggested_revision_count": len([item for item in reviews if str(item.get("suggested_revision", "")).strip()]),
        "issue_count": sum(len(item.get("issue_type") or []) for item in reviews if isinstance(item.get("issue_type"), list)),
    }


def review_items_from_state(state: dict[str, Any]) -> list[dict[str, Any]]:
    reviews = state.get("listeningReviewByKey") or state.get("listening_review_by_key") or {}
    if not isinstance(reviews, dict):
        return []
    return [item for item in reviews.values() if isinstance(item, dict)]


def review_rows_from_state(render_set_id: str, state: dict[str, Any]) -> list[dict[str, str]]:
    phrase_data = list_phrases(render_set_id)
    phrases = {phrase.phrase_id: phrase for phrase in phrase_data["phrases"]}
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    rows = []
    for item in review_items_from_state(state):
        phrase_id = str(item.get("phrase_id", ""))
        version_id = str(item.get("version_id") or item.get("active_version_id") or "")
        if not phrase_id or not version_id:
            continue
        phrase = phrases.get(phrase_id)
        rows.append(
            {
                "review_id": f"R2_REVIEW_{phrase_id}_{version_id}",
                "render_set_id": render_set_id,
                "phrase_id": phrase_id,
                "section_id": phrase.section_id if phrase else "",
                "event_range": phrase.event_range if phrase else "",
                "active_version_id": version_id,
                "preferred_version_id": str(item.get("preferred_version_id") or preferred.get(phrase_id, "")),
                "quick_judgement": "" if item.get("quick_judgement") is None else str(item.get("quick_judgement", "")),
                "issue_type": json.dumps(item.get("issue_type") or [], ensure_ascii=False),
                "severity": str(item.get("severity") or "low"),
                "comment": str(item.get("comment", "")),
                "suggested_revision": str(item.get("suggested_revision", "")),
                "reviewer": str(item.get("reviewer") or "human"),
                "reviewed_at": str(item.get("reviewed_at") or ""),
                "updated_at": str(item.get("updated_at") or item.get("reviewed_at") or ""),
            }
        )
    return rows


def preferred_versions_from_state(state: dict[str, Any], review_rows: list[dict[str, str]]) -> dict[str, str]:
    preferred = state.get("preferredVersionByPhrase") or state.get("preferred_version_by_phrase") or {}
    if not isinstance(preferred, dict):
        preferred = {}
    result = {str(key): str(value) for key, value in preferred.items() if value}
    for row in review_rows:
        phrase_id = row.get("phrase_id", "")
        version_id = row.get("preferred_version_id", "")
        if phrase_id and version_id and phrase_id not in result:
            result[phrase_id] = version_id
    return result


def boundary_status_from_state(state: dict[str, Any]) -> dict[str, str]:
    boundary = state.get("boundaryStatusByKey") or state.get("boundary_status_by_key") or {}
    if not isinstance(boundary, dict):
        return {}
    result: dict[str, str] = {}
    for key, value in boundary.items():
        if not value:
            continue
        raw_key = str(key)
        result[raw_key] = str(value)
        if "::" in raw_key:
            result[raw_key.replace("::", ":", 1)] = str(value)
        elif ":" in raw_key:
            result[raw_key.replace(":", "::", 1)] = str(value)
    return result


def phrase_structure_rows(render_set_id: str, flags: dict[str, str] | None = None) -> list[dict[str, str]]:
    phrase_data = list_phrases(render_set_id)
    row_flags = flags or string_safety_flags()
    rows = []
    for phrase in phrase_data["phrases"]:
        rows.append(
            {
                "section_id": phrase.section_id,
                "section_label": phrase.section_id,
                "phrase_id": phrase.phrase_id,
                "phrase_label": phrase.phrase_label,
                "event_range": phrase.event_range,
                **row_flags,
            }
        )
    return rows


def render_phrase_alignment_table(alignments: list[R2RenderPhraseAlignment], flags: dict[str, str] | None = None) -> dict[str, Any]:
    row_flags = flags or string_safety_flags()
    rows = []
    for item in alignments:
        rows.append(
            {
                "render_set_id": item.render_set_id,
                "version_id": item.version_id,
                "phrase_id": item.phrase_id,
                "section_id": item.section_id,
                "event_range": item.event_range,
                "start_s": f"{item.start_s:.3f}",
                "end_s": f"{item.end_s:.3f}",
                "phrase_play_start_s": f"{(item.phrase_play_start_s if item.phrase_play_start_s is not None else item.start_s):.3f}",
                "phrase_play_end_s": f"{(item.phrase_play_end_s if item.phrase_play_end_s is not None else item.end_s):.3f}",
                "phrase_tail_end_s": f"{(item.phrase_tail_end_s if item.phrase_tail_end_s is not None else item.end_s):.3f}",
                "next_phrase_first_attack_s": "" if item.next_phrase_first_attack_s is None else f"{item.next_phrase_first_attack_s:.3f}",
                "phrase_end_policy": item.phrase_end_policy,
                "boundary_source": item.boundary_source,
                "review_status": item.review_status,
                **row_flags,
            }
        )
    return table_from_rows("render_phrase_alignment.csv", rows)


def phrase_boundary_decision_table(alignments: list[R2RenderPhraseAlignment], boundary_status: dict[str, str], flags: dict[str, str] | None = None) -> dict[str, Any]:
    row_flags = flags or string_safety_flags()
    rows = []
    for item in alignments:
        key = f"{item.phrase_id}:{item.version_id}"
        alt_key = f"{item.phrase_id}::{item.version_id}"
        rows.append(
            {
                "render_set_id": item.render_set_id,
                "version_id": item.version_id,
                "phrase_id": item.phrase_id,
                "section_id": item.section_id,
                "boundary_status": boundary_status.get(key) or boundary_status.get(alt_key) or item.review_status,
                "phrase_start_s": f"{item.start_s:.3f}",
                "phrase_end_s": f"{item.end_s:.3f}",
                "phrase_play_start_s": f"{(item.phrase_play_start_s if item.phrase_play_start_s is not None else item.start_s):.3f}",
                "phrase_play_end_s": f"{(item.phrase_play_end_s if item.phrase_play_end_s is not None else item.end_s):.3f}",
                "phrase_tail_end_s": f"{(item.phrase_tail_end_s if item.phrase_tail_end_s is not None else item.end_s):.3f}",
                "next_phrase_first_attack_s": "" if item.next_phrase_first_attack_s is None else f"{item.next_phrase_first_attack_s:.3f}",
                "phrase_end_policy": item.phrase_end_policy,
                "breath_points_s": ";".join(f"{value:.3f}" for value in item.breath_points_s),
                "cadence_point_s": "" if item.cadence_point_s is None else f"{item.cadence_point_s:.3f}",
                "review_status": "draft",
                **row_flags,
            }
        )
    return table_from_rows("phrase_boundary_decision.csv", rows)


def preferred_rows_from_map(render_set_id: str, preferred: dict[str, str], flags: dict[str, str] | None = None) -> list[dict[str, str]]:
    row_flags = flags or string_safety_flags()
    return [
        {"render_set_id": render_set_id, "phrase_id": phrase_id, "preferred_version_id": version_id, **row_flags}
        for phrase_id, version_id in preferred.items()
    ]


def issue_rows_from_reviews(review_rows: list[dict[str, str]], flags: dict[str, str] | None = None) -> list[dict[str, str]]:
    row_flags = flags or string_safety_flags()
    rows = []
    for review in review_rows:
        for issue in parse_issue_type(review.get("issue_type", "")):
            rows.append(
                {
                    "review_id": review.get("review_id", ""),
                    "phrase_id": review.get("phrase_id", ""),
                    "version_id": review.get("active_version_id", ""),
                    "section_id": review.get("section_id", ""),
                    "issue_type": issue,
                    "severity": review.get("severity", "medium"),
                    "comment": review.get("comment", ""),
                    "suggested_revision": review.get("suggested_revision", ""),
                    **row_flags,
                }
            )
    return rows


def revision_rows_from_reviews(review_rows: list[dict[str, str]], preferred: dict[str, str], flags: dict[str, str] | None = None) -> list[dict[str, str]]:
    row_flags = flags or string_safety_flags()
    rows = []
    for review in review_rows:
        reason = review.get("suggested_revision", "").strip()
        phrase_id = review.get("phrase_id", "")
        version_id = review.get("active_version_id", "")
        if not reason or not phrase_id or not version_id:
            continue
        rows.append(
            {
                "revision_id": f"R2_REVISION_{phrase_id}_{version_id}",
                "render_set_id": review.get("render_set_id", ""),
                "from_version_id": "E_REVIEWED" if version_id == "F_FINAL_REVIEWED" else version_id,
                "to_version_id": "F_FINAL_REVIEWED" if version_id == "F_FINAL_REVIEWED" else preferred.get(phrase_id, review.get("preferred_version_id", "")),
                "phrase_id": phrase_id,
                "section_id": review.get("section_id", ""),
                "event_range": review.get("event_range", ""),
                "change_type": "other",
                "reason": reason,
                **row_flags,
            }
        )
    return rows


def ensure_draft_flags(rows: list[dict[str, str]], flags: dict[str, str] | None = None) -> list[dict[str, str]]:
    row_flags = flags or string_safety_flags()
    return [dict(row) | row_flags for row in rows]


def string_safety_flags(state: dict[str, Any] | None = None) -> dict[str, str]:
    state = state or {}
    f_completed = bool(state.get("f_generation_completed")) or state.get("f_version_id") == "F_FINAL_REVIEWED"
    f_pending = not f_completed if "f_generation_pending" not in state else bool(state.get("f_generation_pending"))
    f_not_generated = not f_completed if "f_not_generated" not in state else bool(state.get("f_not_generated"))
    return {
        "review_status": "draft",
        "gpt_review_pending": "true",
        "e_revision_plan_generated": "false",
        "e_generated": "false",
        "f_generation_pending": json_bool(f_pending),
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_not_generated": json_bool(f_not_generated),
        "f_generation_completed": json_bool(f_completed),
        "f_version_id": "F_FINAL_REVIEWED" if f_completed else "",
        "experimental_render": "true",
        "review_only": "true",
        "production_grade": "false",
    }


def json_bool(value: bool) -> str:
    return "true" if value else "false"


def table_from_rows(file: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    return {"file": file, "columns": columns, "rows": rows}


def write_export_tables(out_dir: Path, tables: dict[str, Any]) -> list[Path]:
    files: list[Path] = []
    for file_name in expected_export_files():
        table = tables.get(file_name)
        if not isinstance(table, dict):
            continue
        path = out_dir / file_name
        if file_name.endswith(".yaml"):
            files.append(write_text(path, table_to_yaml(table)))
        else:
            files.append(write_table_csv(path, table))
    return files


def write_table_csv(path: Path, table: dict[str, Any]) -> Path:
    columns = [str(item) for item in table.get("columns", [])]
    rows = table.get("rows", [])
    if not columns:
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def table_to_yaml(table: dict[str, Any]) -> str:
    columns = [str(item) for item in table.get("columns", [])]
    rows = table.get("rows", [])
    lines = [f"file: {json.dumps(table.get('file', ''), ensure_ascii=False)}", "rows:"]
    for row in rows:
        lines.append("  -")
        for column in columns:
            lines.append(f"      {column}: {json.dumps(row.get(column, ''), ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


def write_review_state_manifest(latest_dir: Path, state: dict[str, Any], files: list[Path], archive_dir: Path) -> Path:
    provenance = state.get("provenance", {}) if isinstance(state.get("provenance"), dict) else {}
    counts = canonical_state_counts(state)
    canonical_state_path = latest_dir / "r2_review_state.latest.json"
    f_completed = bool(state.get("f_generation_completed")) or state.get("f_version_id") == "F_FINAL_REVIEWED"
    f_pending = not f_completed if "f_generation_pending" not in state else bool(state.get("f_generation_pending"))
    f_not_generated = not f_completed if "f_not_generated" not in state else bool(state.get("f_not_generated"))
    manifest = {
        "canonical_source": "r2_review_state.latest.json",
        "canonical_state_path": str(canonical_state_path),
        "generated_exports_path": str(latest_dir),
        "active_render_set_id": state.get("render_set_id"),
        "render_set_id": state.get("render_set_id"),
        "saved_at": state.get("saved_at") or state.get("provenance", {}).get("restored_at"),
        "generated_at": now(),
        "created_at": state.get("saved_at") or provenance.get("restored_at") or now(),
        "restored_at": provenance.get("restored_at", ""),
        "restored_from_exports": provenance.get("restored_from_exports", False),
        "source_export_dir": provenance.get("source_export_dir", ""),
        "review_count": counts["review_count"],
        "phrase_count": counts["phrase_count"],
        "preferred_version_count": counts["preferred_version_count"],
        "suggested_revision_count": counts["suggested_revision_count"],
        "issue_count": counts["issue_count"],
        "current_page_load_source": provenance.get("current_page_load_source") or "engineering_dir_latest",
        "stale_sources_quarantined": provenance.get("stale_sources_quarantined", []),
        "stale_sources_deleted": provenance.get("stale_sources_deleted", []),
        "stale_sources_moved": provenance.get("stale_sources_moved", []),
        "warning_count": len(provenance.get("restore_warnings", [])),
        "active_phrase_id": state.get("active_phrase_id", ""),
        "active_version_id": state.get("active_version_id", ""),
        "latest_dir": str(latest_dir),
        "archive_dir": str(archive_dir),
        "archive_path": str(archive_dir),
        "files": [path.name for path in files],
        "restore_warnings": provenance.get("restore_warnings", []),
        "canonical_dedupe_report": state.get("canonical_dedupe_report", {}),
        "duplicate_keys_found": (state.get("canonical_dedupe_report", {}) or {}).get("duplicate_keys_found", []) if isinstance(state.get("canonical_dedupe_report"), dict) else [],
        "duplicate_rows_removed_or_archived": (state.get("canonical_dedupe_report", {}) or {}).get("duplicate_rows_removed_or_archived", 0) if isinstance(state.get("canonical_dedupe_report"), dict) else 0,
        "no_downloads_policy": True,
        "gpt_review_pending": True,
        "e_revision_plan_generated": False,
        "e_generated": False,
        "f_generation_pending": f_pending,
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_not_generated": f_not_generated,
        "f_generation_completed": f_completed,
        "f_version_id": "F_FINAL_REVIEWED" if f_completed else "",
        "experimental_render": True,
        "production_grade": False,
        **SAFETY,
    }
    path = latest_dir / "r2_review_state_manifest.json"
    write_json(path, manifest)
    return path


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def copy_latest_to_archive(latest_dir: Path, archive_dir: Path) -> None:
    for path in latest_dir.iterdir():
        if path.is_file():
            shutil.copy2(path, archive_dir / path.name)


def write_json(path: Path, data: dict[str, Any]) -> Path:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def safe_timestamp(value: str) -> str:
    return archive_timestamp(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> Path:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_text(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def yaml_dump(data: Any, indent: int = 0) -> str:
    if hasattr(data, "model_dump"):
        data = data.model_dump()
    if isinstance(data, dict):
        lines = []
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(" " * indent + f"{key}:")
                lines.append(yaml_dump(value, indent + 2).rstrip())
            else:
                lines.append(" " * indent + f"{key}: {json.dumps(value, ensure_ascii=False)}")
        return "\n".join(lines) + "\n"
    if isinstance(data, list):
        lines = []
        for item in data:
            if hasattr(item, "model_dump"):
                item = item.model_dump()
            if isinstance(item, dict):
                lines.append(" " * indent + "-")
                lines.append(yaml_dump(item, indent + 2).rstrip())
            else:
                lines.append(" " * indent + f"- {json.dumps(item, ensure_ascii=False)}")
        return "\n".join(lines) + "\n"
    return " " * indent + json.dumps(data, ensure_ascii=False) + "\n"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def now_path() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def archive_timestamp(value: str | None = None) -> str:
    if value:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y%m%d_%H%M%S")
        except ValueError:
            pass
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def safe_name(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_").replace("..", "_")


def _require_render_set(render_set_id: str) -> None:
    intake = load_intake_index()
    if intake and render_set_id == intake["render_set_id"]:
        return
    if render_set_id != RENDER_SET_ID:
        raise ValueError(f"unknown R2 render_set_id: {render_set_id}")


def _require_render_set_or_intake(render_set_id: str) -> None:
    _require_render_set(render_set_id)
