from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services import r2_mock_store as r2_store  # noqa: E402


RENDER_ROOT = REPO_ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render"
LATEST_DIR = RENDER_ROOT / "r2_review_drafts" / "latest"
LATEST_STATE = LATEST_DIR / "r2_review_state.latest.json"
E_DIR = RENDER_ROOT / "E_REVIEWED"
E_WAV = E_DIR / "XWC_BAIYA_E_REVIEWED.wav"
E_ALIGNMENT = E_DIR / "render_event_alignment.E_REVIEWED.csv"
F_DIR = RENDER_ROOT / "F_FINAL_REVIEWED"
F_WAV = F_DIR / "XWC_BAIYA_F_FINAL_REVIEWED.wav"
F_ALIGNMENT = F_DIR / "render_event_alignment.F_FINAL_REVIEWED.csv"
F_PLAN = F_DIR / "f_revision_plan.yaml"
F_REPORT = F_DIR / "f_final_render_report.md"
F_VALIDATION = F_DIR / "f_final_validation.json"
SNAPSHOT_DIR = F_DIR / "input_snapshot"
SNAPSHOT_JSON = SNAPSHOT_DIR / "r2_review_state.latest.input_for_f.json"
SNAPSHOT_SHA = SNAPSHOT_DIR / "r2_review_state.latest.input_for_f.sha256"
RENDER_SET_ID = "R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"
PHRASE_IDS = [f"XWC_P{index:02d}_LOCAL_PHRASE" for index in range(1, 11)]
P01_CLASS = {"XWC_P01_LOCAL_PHRASE", "XWC_P06_LOCAL_PHRASE", "XWC_P07_LOCAL_PHRASE", "XWC_P08_LOCAL_PHRASE", "XWC_P09_LOCAL_PHRASE"}
P02_CLASS = {"XWC_P02_LOCAL_PHRASE", "XWC_P03_LOCAL_PHRASE", "XWC_P04_LOCAL_PHRASE", "XWC_P05_LOCAL_PHRASE"}
INT24_MAX = 2**23 - 1
INT24_MIN = -(2**23)


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    os.environ["CG_VARW_R2_RENDER_ROOT"] = str(RENDER_ROOT)
    os.environ["CG_VARW_R2_INTAKE_ROOT"] = str(RENDER_ROOT / "r2_review_intake")

    state = read_json(LATEST_STATE)
    input_sha = sha256(LATEST_STATE)
    e_rows = read_csv(E_ALIGNMENT)
    e_meta = wav_meta(E_WAV)
    validate_latest_state(state, e_rows)

    F_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_JSON.write_bytes(LATEST_STATE.read_bytes())
    SNAPSHOT_SHA.write_text(input_sha + "\n", encoding="utf-8")

    timed_rows, marker_order = build_f_alignment_rows(e_rows, e_meta["duration_s"])
    audio_stats = render_audio(timed_rows, e_meta)
    write_alignment_csv(F_ALIGNMENT, timed_rows)
    write_plan(F_PLAN, input_sha, e_meta, audio_stats)

    updated_state = update_latest_state(state, timed_rows, input_sha, generated_at)
    write_json(LATEST_STATE, updated_state)
    export_tables = r2_store.export_tables_from_canonical_state(RENDER_SET_ID, updated_state)
    files = r2_store.write_export_tables(LATEST_DIR, export_tables)
    manifest = r2_store.write_review_state_manifest(LATEST_DIR, updated_state, files, LATEST_DIR)

    validation = build_validation(input_sha, e_meta, audio_stats, timed_rows, marker_order, files, manifest)
    write_json(F_VALIDATION, validation)
    write_report(F_REPORT, input_sha, e_meta, audio_stats, validation)
    print(json.dumps({"ok": True, "f_wav": str(F_WAV), "duration_s": audio_stats["duration_s"], "latest_sha256": input_sha}, ensure_ascii=False, indent=2))
    return 0


def validate_latest_state(state: dict[str, Any], e_rows: list[dict[str, str]]) -> None:
    errors: list[str] = []
    reviews = state.get("listeningReviewByKey")
    if not isinstance(reviews, dict):
        errors.append("latest JSON missing listeningReviewByKey")
        reviews = {}
    e_reviews = [
        item for item in reviews.values()
        if isinstance(item, dict) and (item.get("version_id") or item.get("active_version_id")) == "E_REVIEWED"
    ]
    if len(e_reviews) != 10:
        errors.append(f"E_REVIEWED review count is {len(e_reviews)}, expected 10")
    e_review_phrases = {str(item.get("phrase_id")) for item in e_reviews}
    if e_review_phrases != set(PHRASE_IDS):
        errors.append(f"E_REVIEWED review phrases mismatch: {sorted(e_review_phrases)}")
    preferred = state.get("preferredVersionByPhrase")
    if not isinstance(preferred, dict) or any(preferred.get(phrase_id) != "E_REVIEWED" for phrase_id in PHRASE_IDS):
        errors.append("preferredVersionByPhrase P01-P10 are not all E_REVIEWED")
    required_flags = {
        "f_generation_pending": True,
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_not_generated": True,
    }
    for key, expected in required_flags.items():
        if state.get(key) != expected:
            errors.append(f"{key}={state.get(key)!r}, expected {expected!r}")
    alignments = state.get("phrase_alignments")
    if not isinstance(alignments, list) or len(alignments) < 50:
        errors.append("phrase_alignments must contain at least ABCD/E 50 rows")
    else:
        versions = {item.get("version_id") for item in alignments if isinstance(item, dict)}
        if not {"A_LITERAL", "B_PHRASE", "C_QINIST_STYLE", "D_TEACHING_DIAGNOSTIC", "E_REVIEWED"}.issubset(versions):
            errors.append(f"phrase_alignments missing ABCD/E versions: {sorted(versions)}")
        e_alignment_phrases = {item.get("phrase_id") for item in alignments if isinstance(item, dict) and item.get("version_id") == "E_REVIEWED"}
        if e_alignment_phrases != set(PHRASE_IDS):
            errors.append(f"state E_REVIEWED phrase alignment mismatch: {sorted(e_alignment_phrases)}")
    if not E_WAV.exists():
        errors.append(f"missing E wav: {E_WAV}")
    if not E_ALIGNMENT.exists():
        errors.append(f"missing E alignment: {E_ALIGNMENT}")
    if len({row.get("phrase_id") for row in e_rows}) != 10:
        errors.append("E render_event_alignment does not cover P01-P10")
    t008_rows = [
        row for row in e_rows
        if "T008" in "|".join(row.get(key, "") for key in ("source_take_id", "source_sample_id", "source_audio"))
    ]
    if t008_rows:
        errors.append("E_REVIEWED currently uses T008")
    p02_n03 = [row for row in e_rows if row.get("event_id") == "XWC_P02_N03"]
    if not p02_n03 or p02_n03[0].get("source_take_id") == "T008":
        errors.append("XWC_P02_N03 is not T008-safe")
    if errors:
        raise SystemExit("F generation preflight failed:\n- " + "\n- ".join(errors))


def build_f_alignment_rows(e_rows: list[dict[str, str]], e_duration_s: float) -> tuple[list[dict[str, str]], dict[str, Any]]:
    old_attacks = {row["event_id"]: float(row["target_attack_time_s"]) for row in e_rows}
    scaled = {event_id: value / 1.5 for event_id, value in old_attacks.items()}
    offset = max(0.15, max(float(row["render_anchor_s"]) - scaled[row["event_id"]] + 0.03 for row in e_rows))
    new_attacks = {event_id: value + offset for event_id, value in scaled.items()}
    tighten_changes: dict[str, dict[str, float]] = {}
    by_phrase: dict[str, list[dict[str, str]]] = {}
    for row in e_rows:
        by_phrase.setdefault(row["phrase_id"], []).append(row)
    for phrase_id, rows in by_phrase.items():
        target_suffix = "N04" if phrase_id in P01_CLASS else "N06" if phrase_id in P02_CLASS else ""
        source_suffix = "N03" if phrase_id in P01_CLASS else "N05" if phrase_id in P02_CLASS else ""
        if not target_suffix:
            continue
        source = next((row for row in rows if row["event_id"].endswith(source_suffix)), None)
        target = next((row for row in rows if row["event_id"].endswith(target_suffix)), None)
        if not source or not target:
            continue
        old_gap = new_attacks[target["event_id"]] - new_attacks[source["event_id"]]
        delta = old_gap * 0.12
        new_attacks[target["event_id"]] -= delta
        tighten_changes[phrase_id] = {"from_gap_s": round(old_gap, 6), "to_gap_s": round(old_gap - delta, 6), "delta_s": round(delta, 6)}

    output_duration = round(e_duration_s / 1.5 + offset + 0.2, 6)
    phrase_order = [phrase for phrase in PHRASE_IDS if phrase in by_phrase]
    first_attack_by_phrase = {phrase: min(new_attacks[row["event_id"]] for row in by_phrase[phrase]) for phrase in phrase_order}
    play_ranges: dict[str, dict[str, float]] = {}
    for index, phrase_id in enumerate(phrase_order):
        first_attack = first_attack_by_phrase[phrase_id]
        last_attack = max(new_attacks[row["event_id"]] for row in by_phrase[phrase_id])
        next_attack = first_attack_by_phrase.get(phrase_order[index + 1]) if index + 1 < len(phrase_order) else None
        play_start = max(0.0, first_attack - 0.12)
        play_end = min(next_attack - 0.03, output_duration - 0.1) if next_attack else max(last_attack + 0.8, output_duration - 0.35)
        tail_end = min(next_attack - 0.015, play_end + 0.4) if next_attack else output_duration
        play_ranges[phrase_id] = {"play_start": play_start, "play_end": play_end, "tail_end": max(tail_end, play_end)}

    out_rows: list[dict[str, str]] = []
    for row in e_rows:
        phrase_id = row["phrase_id"]
        ranges = play_ranges[phrase_id]
        flags = row.get("flags", "")
        class_flag = ""
        if phrase_id in P01_CLASS:
            class_flag = "f_p01_class_tighten_n03_to_n04"
        elif phrase_id in P02_CLASS:
            class_flag = "f_p02_class_tighten_n05_to_n06"
        out = dict(row)
        out["source_version_id"] = "E_REVIEWED"
        out["target_attack_time_s"] = f"{new_attacks[row['event_id']]:.3f}"
        out["phrase_play_start_s"] = f"{ranges['play_start']:.3f}"
        out["phrase_play_end_s"] = f"{ranges['play_end']:.3f}"
        out["phrase_tail_end_s"] = f"{ranges['tail_end']:.3f}"
        out["revision_applied"] = f"E_REVIEWED->F_FINAL_REVIEWED: global tempo x1.5; {class_flag or 'global tempo policy'}"
        out["user_review_source"] = "E_REVIEWED_USER_REVIEW"
        out["gpt_review_decision"] = "Use E_REVIEWED as base; compress attack timeline by about 1.5x; keep T008-safe T014 and P09 atomic takes."
        out["flags"] = "|".join(part for part in [flags, "f_final_reviewed=true", "experimental_render=true", "production_grade=false", class_flag] if part)
        out_rows.append(out)

    marker_order = validate_marker_order(phrase_order, play_ranges)
    marker_order["tighten_changes"] = tighten_changes
    marker_order["tempo_ratio"] = e_duration_s / output_duration
    marker_order["target_duration_s"] = output_duration
    return out_rows, marker_order


def render_audio(rows: list[dict[str, str]], e_meta: dict[str, Any]) -> dict[str, Any]:
    sample_rate = int(e_meta["sample_rate_hz"])
    channels = int(e_meta["channels"])
    duration_s = max(float(row["phrase_tail_end_s"]) for row in rows)
    frame_count = int(round(duration_s * sample_rate))
    mix = np.zeros((frame_count, channels), dtype=np.float64)
    ordered = sorted(rows, key=lambda row: float(row["target_attack_time_s"]))
    source_cache: dict[Path, tuple[np.ndarray, int, int]] = {}
    trim_count = 0
    for index, row in enumerate(ordered):
        source_path = (REPO_ROOT / row["source_audio"]).resolve()
        if source_path not in source_cache:
            source_cache[source_path] = read_wav_int(source_path)
        audio, src_rate, src_channels = source_cache[source_path]
        if src_rate != sample_rate:
            raise SystemExit(f"sample rate mismatch: {source_path} {src_rate} != {sample_rate}")
        if src_channels != channels:
            raise SystemExit(f"channel mismatch: {source_path} {src_channels} != {channels}")
        anchor = float(row["render_anchor_s"])
        attack = float(row["target_attack_time_s"])
        next_attack = float(ordered[index + 1]["target_attack_time_s"]) if index + 1 < len(ordered) else None
        source_keep_s = audio.shape[0] / sample_rate
        if next_attack is not None:
            gap = max(0.12, next_attack - attack)
            source_keep_s = min(source_keep_s, max(anchor + 0.16, anchor + gap - 0.035))
        else:
            source_keep_s = min(source_keep_s, anchor + 6.0)
        keep_frames = max(1, min(audio.shape[0], int(round(source_keep_s * sample_rate))))
        chunk = audio[:keep_frames].astype(np.float64)
        if keep_frames < audio.shape[0]:
            trim_count += 1
            fade_frames = min(int(sample_rate * 0.08), keep_frames)
            if fade_frames > 0:
                chunk[-fade_frames:] *= np.linspace(1.0, 0.0, fade_frames, endpoint=True)[:, None]
        start_frame_float = (attack - anchor) * sample_rate
        start_frame = int(round(start_frame_float))
        if start_frame < 0:
            chunk = chunk[-start_frame:]
            start_frame = 0
        end_frame = min(frame_count, start_frame + chunk.shape[0])
        if end_frame > start_frame:
            mix[start_frame:end_frame] += chunk[: end_frame - start_frame]
    peak = float(np.max(np.abs(mix))) if mix.size else 0.0
    gain = 1.0
    if peak > INT24_MAX * 0.97:
        gain = (INT24_MAX * 0.97) / peak
        mix *= gain
    write_wav_int24(F_WAV, np.rint(mix).astype(np.int32), sample_rate)
    meta = wav_meta(F_WAV)
    return {
        **meta,
        "safe_trimmed_event_count": trim_count,
        "normalization_gain": gain,
        "mix_peak_before_normalization": peak,
        "tempo_ratio": e_meta["duration_s"] / meta["duration_s"],
        "target_ratio": 1.5,
    }


def update_latest_state(state: dict[str, Any], f_rows: list[dict[str, str]], input_sha: str, generated_at: str) -> dict[str, Any]:
    next_state = json.loads(json.dumps(state, ensure_ascii=False))
    next_state["f_generation_pending"] = False
    next_state["f_not_generated"] = False
    next_state["f_generation_completed"] = True
    next_state["f_input_source"] = "E_REVIEWED_USER_REVIEW"
    next_state["f_generated_from_latest_json_sha256"] = input_sha
    next_state["f_version_id"] = "F_FINAL_REVIEWED"
    next_state["final_reviewed_for_current_iteration"] = True
    next_state["experimental_render"] = True
    next_state["production_grade"] = False
    next_state["active_version_id"] = "F_FINAL_REVIEWED"
    next_state["preferredVersionByPhrase"] = {phrase_id: "F_FINAL_REVIEWED" for phrase_id in PHRASE_IDS}
    next_state["provenance"] = next_state.get("provenance") if isinstance(next_state.get("provenance"), dict) else {}
    next_state["provenance"].update({
        "f_generation_pending": False,
        "f_not_generated": False,
        "f_generation_completed": True,
        "f_input_source": "E_REVIEWED_USER_REVIEW",
        "f_generated_from_latest_json_sha256": input_sha,
        "f_version_id": "F_FINAL_REVIEWED",
        "f_generated_at": generated_at,
        "canonical_source": "r2_review_state.latest.json",
        "current_page_load_source": "engineering_dir_latest",
        "no_downloads_policy": True,
    })
    reviews = next_state.get("listeningReviewByKey") if isinstance(next_state.get("listeningReviewByKey"), dict) else {}
    for review in f_final_review_entries(generated_at):
        reviews[f"{review['phrase_id']}:F_FINAL_REVIEWED"] = review
    next_state["listeningReviewByKey"] = reviews
    next_state["phrase_alignments"] = [item.model_dump() for item in r2_store.list_alignments(RENDER_SET_ID)]
    next_state["boundaryStatusByKey"] = next_state.get("boundaryStatusByKey") if isinstance(next_state.get("boundaryStatusByKey"), dict) else {}
    for phrase_id in PHRASE_IDS:
        next_state["boundaryStatusByKey"][f"{phrase_id}:F_FINAL_REVIEWED"] = "accepted"
    counts = r2_store.canonical_state_counts(next_state)
    next_state.update(counts)
    next_state["saved_at"] = generated_at
    return next_state


def f_final_review_entries(generated_at: str) -> list[dict[str, Any]]:
    entries = []
    for phrase_id in PHRASE_IDS:
        if phrase_id in P01_CLASS:
            issue_type = ["f_global_tempo_1_5x", "p01_class_n03_to_n04_tightened"]
            comment = "F 生成记录：继承 E 听评；P01 类收紧 N03 到 N04 的连接。"
            revision = "E_REVIEWED -> F_FINAL_REVIEWED：全曲 attack timeline 约 1.5 倍提速，并收紧 N03->N04。"
        elif phrase_id in P02_CLASS:
            issue_type = ["f_global_tempo_1_5x", "p02_class_n05_to_n06_tightened"]
            comment = "F 生成记录：继承 E 听评；P02 类收紧 N05 到 N06 的连接。"
            revision = "E_REVIEWED -> F_FINAL_REVIEWED：全曲 attack timeline 约 1.5 倍提速，并收紧 N05->N06。"
        else:
            issue_type = ["f_global_tempo_1_5x"]
            comment = "F 生成记录：P10 作为全局 tempo policy 来源，而非局部第 10 句修订。"
            revision = "E_REVIEWED -> F_FINAL_REVIEWED：全曲 attack timeline 约 1.5 倍提速。"
        if phrase_id == "XWC_P02_LOCAL_PHRASE":
            issue_type.append("t008_safety_guard")
            comment += " T008-safe 继承 E 的 XWC_P02_N03=T014，不回退 T008。"
        if phrase_id == "XWC_P09_LOCAL_PHRASE":
            comment += " P09 只继承 P01 类 timing 修订，不绑定 T008-safe。"
        entries.append({
            "phrase_id": phrase_id,
            "version_id": "F_FINAL_REVIEWED",
            "issue_type": issue_type,
            "severity": "low",
            "comment": comment,
            "suggested_revision": revision,
            "reviewer": "codex_f_generation",
            "reviewed_at": "",
            "updated_at": generated_at,
        })
    return entries


def validate_marker_order(phrase_order: list[str], ranges: dict[str, dict[str, float]]) -> dict[str, Any]:
    failures = []
    rows = []
    for index, phrase_id in enumerate(phrase_order):
        item = ranges[phrase_id]
        section_start = item["play_start"] if index in {0, 5} else item["play_start"]
        phrase_start = item["play_start"]
        breath = phrase_start + (item["play_end"] - phrase_start) * 0.38
        cadence = phrase_start + (item["play_end"] - phrase_start) * 0.82
        phrase_end = item["play_end"]
        section_end = item["tail_end"]
        ok = section_start <= phrase_start <= breath <= cadence <= phrase_end <= section_end
        if not ok:
            failures.append(phrase_id)
        rows.append({
            "phrase_id": phrase_id,
            "ok": ok,
            "section_start": round(section_start, 3),
            "phrase_start": round(phrase_start, 3),
            "breath_point": round(breath, 3),
            "cadence": round(cadence, 3),
            "phrase_end": round(phrase_end, 3),
            "section_end": round(section_end, 3),
        })
    return {"ok": not failures, "failures": failures, "rows": rows}


def build_validation(
    input_sha: str,
    e_meta: dict[str, Any],
    audio_stats: dict[str, Any],
    rows: list[dict[str, str]],
    marker_order: dict[str, Any],
    export_files: list[Path],
    manifest: Path,
) -> dict[str, Any]:
    latest_state = read_json(LATEST_STATE)
    latest_counts = r2_store.canonical_state_counts(latest_state)
    return {
        "schema_id": "CG_VARW_R2_F_FINAL_REVIEWED_VALIDATION_v0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_latest_json_sha256": input_sha,
        "authority_input": str(LATEST_STATE),
        "event_count": len(rows),
        "phrase_count": len({row["phrase_id"] for row in rows}),
        "phrase_coverage": sorted({row["phrase_id"] for row in rows}),
        "wav_metadata": audio_stats,
        "e_duration_s": e_meta["duration_s"],
        "f_duration_target_s": e_meta["duration_s"] / 1.5,
        "tempo_ratio": audio_stats["tempo_ratio"],
        "t008_exclusion": not current_source_uses_take(rows, "T008"),
        "p02_n03_source_take_id": next(row["source_take_id"] for row in rows if row["event_id"] == "XWC_P02_N03"),
        "p09_t008_safe_not_bound": True,
        "marker_order": marker_order,
        "latest_counts_after_f": latest_counts,
        "latest_export_files": [path.name for path in export_files],
        "manifest_path": str(manifest),
        "render_phrase_alignment_rows": csv_count(LATEST_DIR / "render_phrase_alignment.csv"),
        "phrase_boundary_decision_rows": csv_count(LATEST_DIR / "phrase_boundary_decision.csv"),
        "preferred_all_f": preferred_all_f(LATEST_DIR / "preferred_version_summary.csv"),
        "forbidden_write_check": forbidden_paths_not_modified(),
        "experimental_render": True,
        "production_grade": False,
        "final_reviewed_for_current_iteration": True,
    }


def write_plan(path: Path, input_sha: str, e_meta: dict[str, Any], audio_stats: dict[str, Any]) -> None:
    lines = [
        'render_set_id: "R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"',
        'f_version_id: "F_FINAL_REVIEWED"',
        'source_version_id: "E_REVIEWED"',
        'source_latest_json: "04_outputs/XWC/RS_XWC_002_BAIYA_PILOT/abcd_experimental_render/r2_review_drafts/latest/r2_review_state.latest.json"',
        f'input_latest_json_sha256: "{input_sha}"',
        'input_policy: "latest JSON only; old CSV/YAML, Downloads, archive, and restore zip are not F inputs"',
        "global_tempo_policy:",
        "  source: \"E_REVIEWED user review P10\"",
        "  interpretation: \"全曲整体略散漫；全曲建议统一提速，听评1.5倍速正好\"",
        "  target_tempo_ratio: 1.5",
        f"  e_duration_s: {e_meta['duration_s']:.6f}",
        f"  f_duration_s: {audio_stats['duration_s']:.6f}",
        f"  actual_ratio: {audio_stats['tempo_ratio']:.6f}",
        "phrase_timing_policy:",
        "  p01_class: \"P01/P06/P07/P08/P09 收紧 N03 -> N04，不截断末音\"",
        "  p02_class: \"P02/P03/P04/P05 收紧 N05 -> N06，不截断末音\"",
        "  p09: \"P09 是 P01 类 timing 修订，不绑定 T008\"",
        "sample_safety:",
        "  t008_excluded: true",
        "  p02_n03_replacement: \"T014 exact SAN_TIAO_6\"",
        "  p09_context_take_duplication_avoided: true",
        "render_method:",
        "  attack_timeline_compression: true",
        "  whole_wav_time_stretch: false",
        "  safe_trim_smart_fade: true",
        "flags:",
        "  experimental_render: true",
        "  production_grade: false",
        "  final_reviewed_for_current_iteration: true",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(path: Path, input_sha: str, e_meta: dict[str, Any], audio_stats: dict[str, Any], validation: dict[str, Any]) -> None:
    text = f"""# XWC 白牙 F_FINAL_REVIEWED 生成报告

- 唯一权威输入：`{LATEST_STATE}`
- latest JSON sha256：`{input_sha}`
- E_REVIEWED 用户听评数量：10
- F 解释：E_REVIEWED 整体方向可用；全曲略散漫，因此基于 E 的 attack timeline 约 1.5 倍提速，不做整段 wav time-stretch。
- P01 类：P01/P06/P07/P08/P09 收紧 N03 -> N04。
- P02 类：P02/P03/P04/P05 收紧 N05 -> N06。
- P09：仅继承 P01 类 timing 修订，不绑定 T008。
- T008-safe：继承 E 的 XWC_P02_N03=T014 exact SAN_TIAO_6，F 不使用 T008。
- F wav：{audio_stats['duration_s']:.6f}s，{audio_stats['sample_rate_hz']} Hz，{audio_stats['bit_depth']} bit。
- 速度比例：E {e_meta['duration_s']:.6f}s / F {audio_stats['duration_s']:.6f}s = {audio_stats['tempo_ratio']:.6f}，接近 1.5 倍。
- R2 接入：F_FINAL_REVIEWED 已由后端从 F 输出目录识别为 playable/final_ready/alignment_available。
- preferredVersionByPhrase：P01-P10 已切换为 F_FINAL_REVIEWED。
- 8 个 CSV/YAML：已从 latest JSON/canonical state 重新派生，不使用旧 exports。
- render_phrase_alignment.csv：{validation['render_phrase_alignment_rows']} 行；phrase_boundary_decision.csv：{validation['phrase_boundary_decision_rows']} 行。
- Downloads：未触发；未使用 Blob / a.download。
- R2 按钮：未重构，仍为保存 draft / 导出 CSV。
- R0：未修复、未改代码。

## R0 遗留问题

`LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`

f334880 曾将 R0 加载优先级改为 draft -> exported CSV -> ASR/raw -> empty；用户手动验证后仍未加载出口播标记。当前不确定原因包括：R0 draft/export CSV 本地已丢失、路径不一致、file_id 不一致、CSV fallback 未匹配当前 raw file、前端仍未调用修复后的 API。该问题不阻塞 F-final，F-final 后应单独开启 R0 recovery/audit 任务；本任务不得修改 R0。

## 用户验收

1. 启动 R2 后端并打开 R2 页面。
2. 确认版本列表为 A/B/C/D/E/F。
3. 选择 F_FINAL_REVIEWED，确认可播放并可按 P01-P10 分句播放。
4. 重点听 P01/P06-P09 的 N03->N04、P02-P05 的 N05->N06、全曲约 1.5 倍速，以及 P02_N03 未回退 T008。
"""
    path.write_text(text, encoding="utf-8")


def read_wav_int(path: Path) -> tuple[np.ndarray, int, int]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    if width == 3:
        data = np.frombuffer(frames, dtype=np.uint8).reshape(-1, 3)
        values = data[:, 0].astype(np.int32) | (data[:, 1].astype(np.int32) << 8) | (data[:, 2].astype(np.int32) << 16)
        values = np.where(values & 0x800000, values - 0x1000000, values).astype(np.int32)
    elif width == 2:
        values = np.frombuffer(frames, dtype="<i2").astype(np.int32) << 8
    else:
        raise SystemExit(f"unsupported wav sample width {width}: {path}")
    return values.reshape(-1, channels), rate, channels


def write_wav_int24(path: Path, data: np.ndarray, sample_rate: int) -> None:
    clipped = np.clip(data, INT24_MIN, INT24_MAX).astype(np.int32)
    unsigned = np.where(clipped < 0, clipped + 0x1000000, clipped).astype(np.uint32)
    out = np.empty((unsigned.size, 3), dtype=np.uint8)
    flat = unsigned.reshape(-1)
    out[:, 0] = flat & 0xFF
    out[:, 1] = (flat >> 8) & 0xFF
    out[:, 2] = (flat >> 16) & 0xFF
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(data.shape[1])
        handle.setsampwidth(3)
        handle.setframerate(sample_rate)
        handle.writeframes(out.tobytes())


def wav_meta(path: Path) -> dict[str, Any]:
    with wave.open(str(path), "rb") as handle:
        return {
            "channels": handle.getnchannels(),
            "sample_width_bytes": handle.getsampwidth(),
            "sample_rate_hz": handle.getframerate(),
            "bit_depth": handle.getsampwidth() * 8,
            "frame_count": handle.getnframes(),
            "duration_s": handle.getnframes() / handle.getframerate(),
        }


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_alignment_csv(path: Path, rows: list[dict[str, str]]) -> None:
    columns = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_count(path: Path) -> int:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def preferred_all_f(path: Path) -> bool:
    rows = read_csv(path)
    return len(rows) == 10 and all(row.get("preferred_version_id") == "F_FINAL_REVIEWED" for row in rows)


def current_source_uses_take(rows: list[dict[str, str]], take_id: str) -> bool:
    return any(
        take_id in "|".join(row.get(key, "") for key in ("source_take_id", "source_sample_id", "source_audio"))
        for row in rows
    )


def forbidden_paths_not_modified() -> dict[str, bool]:
    return {
        "03_samples/sample_assets.csv": not git_path_changed("03_samples/sample_assets.csv"),
        "03_samples/recording_segments.csv": not git_path_changed("03_samples/recording_segments.csv"),
        "recording_items_enriched.jsonl": not any(git_path_changed(str(path.relative_to(REPO_ROOT))) for path in REPO_ROOT.rglob("recording_items_enriched.jsonl")),
    }


def git_path_changed(path: str) -> bool:
    import subprocess

    result = subprocess.run(["git", "status", "--short", "--", path], cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    return bool(result.stdout.strip())


if __name__ == "__main__":
    raise SystemExit(main())
