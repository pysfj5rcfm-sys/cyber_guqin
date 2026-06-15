from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import REVIEW_OUTPUT_ROOT
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
    return PIECES


def list_sessions() -> list[R2Session]:
    return SESSIONS


def list_render_sets() -> list[R2RenderSet]:
    return [RENDER_SET]


def get_render_set(render_set_id: str) -> R2RenderSet:
    _require_render_set(render_set_id)
    return RENDER_SET


def list_versions(render_set_id: str) -> list[R2RenderVersion]:
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
    _require_render_set(render_set_id)
    return {"sections": SECTIONS, "phrases": PHRASES, **SAFETY}


def list_alignments(render_set_id: str) -> list[R2RenderPhraseAlignment]:
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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> Path:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
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


def safe_name(value: str) -> str:
    return value.replace("/", "_").replace("\\", "_").replace("..", "_")


def _require_render_set(render_set_id: str) -> None:
    if render_set_id != RENDER_SET_ID:
        raise ValueError(f"unknown R2 render_set_id: {render_set_id}")
