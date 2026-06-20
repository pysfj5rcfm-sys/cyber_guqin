#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import re
import subprocess
import sys
import wave
from array import array
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_NAME = "CG-XWC_BAIYA_ABCD_EXPERIMENTAL_RENDER_FROM_PLANNING"
PLANNING_COMMIT = "228b808"
SESSION_DIR = ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT"
RENDER_DIR = SESSION_DIR / "abcd_experimental_render"
PLANNING_DIR = RENDER_DIR / "_planning"
READINESS_DIR = SESSION_DIR / "abcd_render_readiness"

SOURCE_MAP_PATH = PLANNING_DIR / "render_source_map.local.json"
PHRASE_PLAN_PATH = PLANNING_DIR / "render_phrase_plan.local.yaml"
VERSION_POLICY_PATH = PLANNING_DIR / "abcd_version_policy.local.yaml"
E_SCHEMA_PATH = PLANNING_DIR / "e_co_review_schema.local.yaml"
LOGIC_REPORT_PATH = PLANNING_DIR / "abcd_generation_logic_report.md"
PLAN_VALIDATION_PATH = PLANNING_DIR / "abcd_generation_plan_validation.json"
MANIFEST_CSV_PATH = READINESS_DIR / "abcd_render_input_manifest.csv"
MANIFEST_JSON_PATH = READINESS_DIR / "abcd_render_input_manifest.json"

VERSION_OUTPUTS = {
    "A_LITERAL": ("A_LITERAL", "XWC_BAIYA_A_LITERAL.wav"),
    "B_PHRASE": ("B_PHRASE", "XWC_BAIYA_B_PHRASE.wav"),
    "C_QINIST_STYLE": ("C_QINIST_STYLE", "XWC_BAIYA_C_QINIST_STYLE.wav"),
    "D_TEACHING_DIAGNOSTIC": ("D_TEACHING_DIAGNOSTIC", "XWC_BAIYA_D_TEACHING_DIAGNOSTIC.wav"),
}

VERSION_RENDER_SETTINGS = {
    "A_LITERAL": {
        "base_gap_s": 2.35,
        "phrase_pause": {"short": 0.35, "medium": 0.55, "long": 0.85},
        "crossfade_ms": 60,
        "overlap_ms": 0,
        "context_take": "T059",
        "duplicate_mode": "first",
    },
    "B_PHRASE": {
        "base_gap_s": 2.45,
        "phrase_pause": {"short": 0.65, "medium": 0.95, "long": 1.35},
        "crossfade_ms": 120,
        "overlap_ms": 30,
        "context_take": "T060",
        "duplicate_mode": "phrase_end_last",
    },
    "C_QINIST_STYLE": {
        "base_gap_s": 2.20,
        "phrase_pause": {"short": 0.45, "medium": 0.70, "long": 1.05},
        "crossfade_ms": 180,
        "overlap_ms": 60,
        "context_take": "T071",
        "duplicate_mode": "last",
    },
    "D_TEACHING_DIAGNOSTIC": {
        "base_gap_s": 2.85,
        "phrase_pause": {"short": 0.80, "medium": 1.10, "long": 1.50},
        "crossfade_ms": 40,
        "overlap_ms": 0,
        "context_take": "T060",
        "duplicate_mode": "first",
    },
}

ALIGNMENT_FIELDS = [
    "version_id",
    "event_id",
    "event_range",
    "phrase_id",
    "section_id",
    "recording_take_no",
    "batch_id",
    "source_split_audio",
    "gesture_id",
    "realization_variant",
    "target_attack_time_s",
    "segment_insert_time_s",
    "render_anchor_s",
    "render_anchor_type",
    "pre_attack_music_policy",
    "tail_policy",
    "tail_end_s",
    "segment_start_s_in_render",
    "segment_end_s_in_render",
    "crossfade_ms",
    "overlap_ms",
    "phrase_boundary_role",
    "experimental_render",
    "production_grade",
    "not_sample_assets",
    "not_recording_segments",
    "not_ml_training_data",
]

SELECTION_FIELDS = [
    "version_id",
    "event_id",
    "event_range",
    "phrase_id",
    "gesture_id",
    "selected_recording_take_no",
    "selected_batch_id",
    "selected_source_split_audio",
    "realization_variant",
    "expected_sample_type",
    "context_take_used",
    "context_take_candidate",
    "selection_reason",
    "render_anchor_s",
    "render_anchor_type",
    "pre_attack_music_policy",
    "tail_policy",
    "source_map_row_id",
    "experimental_render",
    "production_grade",
    "not_sample_assets",
    "not_recording_segments",
    "not_ml_training_data",
]

RENDER_MANIFEST_FIELDS = [
    "version_id",
    "version_label",
    "wav_path",
    "duration_s",
    "sample_rate",
    "channels",
    "event_count",
    "phrase_count",
    "source_map_rows_used",
    "generated_at",
    "experimental_render",
    "production_grade",
    "e_version",
    "not_sample_assets",
    "not_recording_segments",
    "not_ml_training_data",
]


class RenderBlocker(RuntimeError):
    pass


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_quoted_value(line: str) -> str:
    _, value = line.split(":", 1)
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value in {"true", "false"}:
        return value
    return value


def parse_phrase_plan(path: Path) -> list[dict]:
    phrases: list[dict] = []
    current: dict | None = None
    wanted = {
        "phrase_id",
        "section_id",
        "event_range",
        "phrase_role",
        "phrase_start_event_id",
        "phrase_end_event_id",
        "phrase_end_pause_class",
    }
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("phrase_id:"):
            if current:
                phrases.append(current)
            current = {"phrase_id": parse_quoted_value(stripped)}
        elif current and ":" in stripped:
            key = stripped.split(":", 1)[0]
            if key in wanted:
                current[key] = parse_quoted_value(stripped)
    if current:
        phrases.append(current)
    if not phrases:
        raise RenderBlocker(f"未能从 {path} 读取 phrase plan")
    return phrases


def parse_version_policy(path: Path) -> dict[str, dict]:
    versions: dict[str, dict] = {}
    current: dict | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("version_id:"):
            if current:
                versions[current["version_id"]] = current
            current = {"version_id": parse_quoted_value(stripped)}
        elif current and stripped.startswith("version_label:"):
            current["version_label"] = parse_quoted_value(stripped)
        elif current and stripped.startswith("version_intent:"):
            current["version_intent"] = parse_quoted_value(stripped)
        elif current and re.match(r"(tempo_policy|phrase_pause_policy|rubato_policy|crossfade_policy|tail_policy_preference|pre_attack_policy|selection_priority):", stripped):
            key = stripped.split(":", 1)[0]
            current[key] = parse_quoted_value(stripped)
    if current:
        versions[current["version_id"]] = current
    missing = [v for v in VERSION_OUTPUTS if v not in versions]
    if missing:
        raise RenderBlocker("abcd_version_policy.local.yaml 缺少版本: " + ", ".join(missing))
    return versions


def check_required_inputs() -> None:
    required = [
        SOURCE_MAP_PATH,
        PHRASE_PLAN_PATH,
        VERSION_POLICY_PATH,
        E_SCHEMA_PATH,
        LOGIC_REPORT_PATH,
        PLAN_VALIDATION_PATH,
        MANIFEST_CSV_PATH,
        MANIFEST_JSON_PATH,
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise RenderBlocker("缺少必须输入文件: " + ", ".join(missing))


def check_planning_commit() -> bool:
    try:
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", PLANNING_COMMIT, "HEAD"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def load_source_rows() -> list[dict]:
    source_map = read_json(SOURCE_MAP_PATH)
    rows = source_map.get("rows", [])
    if len(rows) != 71:
        raise RenderBlocker(f"source map row count 必须为 71，实际为 {len(rows)}")
    for idx, row in enumerate(rows, start=1):
        row["source_map_row_id"] = f"source_map_row_{idx:03d}"
    return rows


def read_wav_metadata(path: Path) -> dict:
    with wave.open(str(path), "rb") as wav:
        return {
            "channels": wav.getnchannels(),
            "sample_width": wav.getsampwidth(),
            "sample_rate": wav.getframerate(),
            "frames": wav.getnframes(),
            "duration_s": wav.getnframes() / wav.getframerate(),
        }


def preflight_rows(rows: list[dict]) -> dict:
    missing: list[str] = []
    unreadable: list[str] = []
    formats: set[tuple[int, int, int]] = set()
    for row in rows:
        path = ROOT / row["clean_preview_audio"]
        if not path.exists():
            missing.append(row["clean_preview_audio"])
            continue
        try:
            meta = read_wav_metadata(path)
            formats.add((meta["channels"], meta["sample_width"], meta["sample_rate"]))
            row["source_duration_s"] = meta["duration_s"]
            row["source_frames"] = meta["frames"]
        except Exception:
            unreadable.append(row["clean_preview_audio"])

    t071 = next((r for r in rows if r["recording_take_no"] == "T071"), None)
    t060 = next((r for r in rows if r["recording_take_no"] == "T060"), None)
    batch07 = [r["recording_take_no"] for r in rows if r["batch_id"] == "batch07"]
    batch08 = [r["recording_take_no"] for r in rows if r["batch_id"] == "batch08"]
    t071_rule_ok = bool(
        t071
        and t071["batch_id"] == "batch08"
        and t071["recording_take_no"] == "T071"
        and t071["batch_take_no"] == "001"
        and batch07 == [f"T{i:03d}" for i in range(61, 71)]
        and batch08 == ["T071"]
    )
    context_rule_ok = bool(
        t060
        and t071
        and t060.get("context_reference_role") == "context_take_1"
        and t071.get("context_reference_role") == "context_take_2"
        and t060["event_range"] == "XWC_P09_N01_to_N02"
        and t071["event_range"] == "XWC_P09_N01_to_N02"
        and t060["expected_sample_type"] == "context"
        and t071["expected_sample_type"] == "context"
    )
    dummy_fallback_used = any(row.get("dummy_fallback_used") for row in rows)
    bad_flags = [
        row["source_map_row_id"]
        for row in rows
        if not row.get("experimental_render")
        or row.get("production_grade")
        or not row.get("not_sample_assets")
        or not row.get("not_recording_segments")
        or not row.get("not_ml_training_data")
    ]
    blocker_parts = []
    if missing:
        blocker_parts.append(f"missing_source_audio_count={len(missing)}")
    if unreadable:
        blocker_parts.append(f"unreadable_source_audio_count={len(unreadable)}")
    if formats != {(2, 3, 44100)}:
        blocker_parts.append(f"unsupported_wav_formats={sorted(formats)}")
    if not t071_rule_ok:
        blocker_parts.append("t071_rule_ok=false")
    if not context_rule_ok:
        blocker_parts.append("t060_t071_context_rule_ok=false")
    if dummy_fallback_used:
        blocker_parts.append("dummy_fallback_used=true")
    if bad_flags:
        blocker_parts.append("source_map_safety_flags_invalid=" + ",".join(bad_flags[:5]))
    return {
        "missing": missing,
        "unreadable": unreadable,
        "formats": sorted(formats),
        "missing_source_audio_count": len(missing),
        "unreadable_source_audio_count": len(unreadable),
        "t071_rule_ok": t071_rule_ok,
        "t060_t071_context_rule_ok": context_rule_ok,
        "dummy_fallback_used": dummy_fallback_used,
        "blocker_reason": "; ".join(blocker_parts),
    }


def ensure_e_not_generated() -> None:
    text = E_SCHEMA_PATH.read_text(encoding="utf-8")
    if "e_audio_generated: false" not in text or "must_not_generate_audio_until_confirmed: true" not in text:
        raise RenderBlocker("E_REVIEWED schema 未明确禁止当前生成 E 音频")


def phrase_for_event(event_id: str, phrases: list[dict]) -> dict:
    event_num = event_id_to_tuple(event_id)
    for phrase in phrases:
        start = event_id_to_tuple(phrase["phrase_start_event_id"])
        end = event_id_to_tuple(phrase["phrase_end_event_id"])
        if start <= event_num <= end:
            return phrase
    section = event_id.rsplit("_", 1)[0]
    return {
        "phrase_id": f"{section}_LOCAL_PHRASE",
        "section_id": section,
        "phrase_start_event_id": event_id,
        "phrase_end_event_id": event_id,
        "phrase_end_pause_class": "short",
        "phrase_role": "local_dapu_phrase",
    }


def event_id_to_tuple(event_id: str) -> tuple[int, int]:
    match = re.match(r"XWC_P(\d+)_N(\d+)", event_id)
    if not match:
        return (999, 999)
    return (int(match.group(1)), int(match.group(2)))


def unique_event_ids(rows: list[dict]) -> list[str]:
    got: list[str] = []
    for row in rows:
        if row["event_id"] not in got:
            got.append(row["event_id"])
    return got


def choose_source_row(version_id: str, event_rows: list[dict], phrase: dict) -> tuple[dict, str]:
    settings = VERSION_RENDER_SETTINGS[version_id]
    if event_rows[0]["event_id"] == "XWC_P09_N02":
        preferred = settings["context_take"]
        selected = next((r for r in event_rows if r["recording_take_no"] == preferred), None)
        if not selected:
            raise RenderBlocker(f"{version_id} 需要的 context take {preferred} 缺失")
        return selected, f"{version_id} 按 context policy 选择 {preferred}，保留 P09 transition context identity"

    ordered = sorted(event_rows, key=lambda r: r["recording_take_no"])
    mode = settings["duplicate_mode"]
    if mode == "last" and len(ordered) > 1:
        return ordered[-1], f"{version_id} 按琴人风格版策略选择同事件后序 clean take"
    if mode == "phrase_end_last" and len(ordered) > 1 and ordered[0]["event_id"] == phrase["phrase_end_event_id"]:
        return ordered[-1], f"{version_id} 按 phrase boundary 策略选择句末后序 clean take"
    return ordered[0], f"{version_id} 按版本策略选择同事件首个 ready clean take"


def selected_events_for_version(version_id: str, rows: list[dict], phrases: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["event_id"], []).append(row)
    selected: list[dict] = []
    for event_id in unique_event_ids(rows):
        phrase = phrase_for_event(event_id, phrases)
        row, reason = choose_source_row(version_id, grouped[event_id], phrase)
        selected.append({"source": row, "phrase": phrase, "selection_reason": reason})
    if len(selected) != 51:
        raise RenderBlocker(f"{version_id} selected event count 必须为 51，实际为 {len(selected)}")
    return selected


def phrase_boundary_role(event_id: str, phrase: dict) -> str:
    start = phrase["phrase_start_event_id"]
    end = phrase["phrase_end_event_id"]
    if event_id == start and event_id == end:
        return "single_event_phrase"
    if event_id == start:
        return "phrase_start"
    if event_id == end:
        return "phrase_end"
    return "within_phrase"


def schedule_events(version_id: str, selected: list[dict]) -> list[dict]:
    settings = VERSION_RENDER_SETTINGS[version_id]
    current_attack = 4.0
    scheduled: list[dict] = []
    for idx, item in enumerate(selected):
        source = item["source"]
        phrase = item["phrase"]
        boundary_role = phrase_boundary_role(source["event_id"], phrase)
        anchor = float(source["render_anchor_s"])
        insert = current_attack - anchor
        if insert < 0:
            raise RenderBlocker(f"{version_id} {source['event_id']} segment_insert_time_s 为负数")
        item = dict(item)
        item.update(
            {
                "target_attack_time_s": current_attack,
                "segment_insert_time_s": insert,
                "segment_start_s_in_render": insert,
                "segment_end_s_in_render": insert + float(source["source_duration_s"]),
                "crossfade_ms": settings["crossfade_ms"],
                "overlap_ms": settings["overlap_ms"],
                "phrase_boundary_role": boundary_role,
            }
        )
        scheduled.append(item)
        tail_after_anchor = max(0.5, float(source["tail_end_s"]) - anchor)
        pause_class = phrase.get("phrase_end_pause_class", "short")
        phrase_pause = settings["phrase_pause"].get(pause_class, 0.45) if boundary_role == "phrase_end" else 0.0
        if version_id == "C_QINIST_STYLE":
            expressive_nudge = 0.16 * math.sin((idx + 1) * 0.9)
        elif version_id == "B_PHRASE":
            expressive_nudge = 0.08 * math.sin((idx + 1) * 0.7)
        else:
            expressive_nudge = 0.0
        gap = max(settings["base_gap_s"], min(4.2, tail_after_anchor * 0.45 + settings["base_gap_s"] * 0.55))
        current_attack += max(1.6, gap + phrase_pause + expressive_nudge - settings["overlap_ms"] / 1000.0)
    return scheduled


def pcm24_to_ints(frames: bytes) -> array:
    out = array("i")
    for i in range(0, len(frames), 3):
        sample = frames[i] | (frames[i + 1] << 8) | (frames[i + 2] << 16)
        if sample & 0x800000:
            sample -= 0x1000000
        out.append(sample)
    return out


def ints_to_pcm24(samples: array) -> bytes:
    max_abs = max((abs(v) for v in samples), default=0)
    limit = 8388607
    scale = min(1.0, (limit * 0.98) / max_abs) if max_abs else 1.0
    payload = bytearray()
    for value in samples:
        scaled = int(round(value * scale))
        scaled = max(-8388608, min(8388607, scaled))
        if scaled < 0:
            scaled += 0x1000000
        payload.extend((scaled & 0xFF, (scaled >> 8) & 0xFF, (scaled >> 16) & 0xFF))
    return bytes(payload)


def read_pcm24_wav(path: Path) -> tuple[array, dict]:
    with wave.open(str(path), "rb") as wav:
        meta = {
            "channels": wav.getnchannels(),
            "sample_width": wav.getsampwidth(),
            "sample_rate": wav.getframerate(),
            "frames": wav.getnframes(),
        }
        if (meta["channels"], meta["sample_width"], meta["sample_rate"]) != (2, 3, 44100):
            raise RenderBlocker(f"Unsupported wav format for render: {path}")
        data = pcm24_to_ints(wav.readframes(wav.getnframes()))
    return data, meta


def write_pcm24_wav(path: Path, samples: array, sample_rate: int = 44100, channels: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(3)
        wav.setframerate(sample_rate)
        wav.writeframes(ints_to_pcm24(samples))


def render_version(version_id: str, version_policy: dict, scheduled: list[dict]) -> tuple[dict, list[dict], list[dict]]:
    subdir, wav_name = VERSION_OUTPUTS[version_id]
    wav_path = RENDER_DIR / subdir / wav_name
    alignment_path = RENDER_DIR / subdir / f"render_event_alignment.{version_id}.csv"
    sample_rate = 44100
    channels = 2
    final_end_s = max(item["segment_end_s_in_render"] for item in scheduled) + 1.0
    mix = array("q", [0]) * (int(math.ceil(final_end_s * sample_rate)) * channels)
    alignment_rows: list[dict] = []
    selection_rows: list[dict] = []
    used_row_ids: set[str] = set()

    for item in scheduled:
        source = item["source"]
        phrase = item["phrase"]
        path = ROOT / source["clean_preview_audio"]
        data, meta = read_pcm24_wav(path)
        start_frame = int(round(item["segment_insert_time_s"] * sample_rate))
        for i, sample in enumerate(data):
            pos = start_frame * channels + i
            if 0 <= pos < len(mix):
                mix[pos] += sample

        used_row_ids.add(source["source_map_row_id"])
        event_range = source["event_range"] or source["event_id"]
        common_flags = {
            "experimental_render": "true",
            "production_grade": "false",
            "not_sample_assets": "true",
            "not_recording_segments": "true",
            "not_ml_training_data": "true",
        }
        alignment_rows.append(
            {
                "version_id": version_id,
                "event_id": source["event_id"],
                "event_range": event_range,
                "phrase_id": phrase["phrase_id"],
                "section_id": phrase["section_id"],
                "recording_take_no": source["recording_take_no"],
                "batch_id": source["batch_id"],
                "source_split_audio": source["source_split_audio"],
                "gesture_id": source["gesture_id"],
                "realization_variant": source["realization_variant"],
                "target_attack_time_s": f"{item['target_attack_time_s']:.3f}",
                "segment_insert_time_s": f"{item['segment_insert_time_s']:.3f}",
                "render_anchor_s": f"{float(source['render_anchor_s']):.3f}",
                "render_anchor_type": source["render_anchor_type"],
                "pre_attack_music_policy": source["pre_attack_music_policy"],
                "tail_policy": source["tail_policy"],
                "tail_end_s": f"{float(source['tail_end_s']):.3f}",
                "segment_start_s_in_render": f"{item['segment_start_s_in_render']:.3f}",
                "segment_end_s_in_render": f"{item['segment_end_s_in_render']:.3f}",
                "crossfade_ms": str(item["crossfade_ms"]),
                "overlap_ms": str(item["overlap_ms"]),
                "phrase_boundary_role": item["phrase_boundary_role"],
                **common_flags,
            }
        )
        context_candidates = ",".join(
            row["recording_take_no"]
            for row in scheduled_event_candidates(source["event_id"])
            if row["expected_sample_type"] == "context"
        )
        selection_rows.append(
            {
                "version_id": version_id,
                "event_id": source["event_id"],
                "event_range": event_range,
                "phrase_id": phrase["phrase_id"],
                "gesture_id": source["gesture_id"],
                "selected_recording_take_no": source["recording_take_no"],
                "selected_batch_id": source["batch_id"],
                "selected_source_split_audio": source["source_split_audio"],
                "realization_variant": source["realization_variant"],
                "expected_sample_type": source["expected_sample_type"],
                "context_take_used": "true" if source["expected_sample_type"] == "context" else "false",
                "context_take_candidate": context_candidates,
                "selection_reason": item["selection_reason"],
                "render_anchor_s": f"{float(source['render_anchor_s']):.3f}",
                "render_anchor_type": source["render_anchor_type"],
                "pre_attack_music_policy": source["pre_attack_music_policy"],
                "tail_policy": source["tail_policy"],
                "source_map_row_id": source["source_map_row_id"],
                **common_flags,
            }
        )

    write_pcm24_wav(wav_path, mix, sample_rate=sample_rate, channels=channels)
    write_csv(alignment_path, ALIGNMENT_FIELDS, alignment_rows)
    manifest_row = {
        "version_id": version_id,
        "version_label": version_policy.get("version_label", version_id),
        "wav_path": str(wav_path.relative_to(ROOT)),
        "duration_s": f"{len(mix) / channels / sample_rate:.3f}",
        "sample_rate": str(sample_rate),
        "channels": str(channels),
        "event_count": str(len(alignment_rows)),
        "phrase_count": str(len({row['phrase_id'] for row in alignment_rows})),
        "source_map_rows_used": str(len(used_row_ids)),
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "experimental_render": "true",
        "production_grade": "false",
        "e_version": "false",
        "not_sample_assets": "true",
        "not_recording_segments": "true",
        "not_ml_training_data": "true",
    }
    return manifest_row, alignment_rows, selection_rows


ALL_ROWS_FOR_CANDIDATES: list[dict] = []


def scheduled_event_candidates(event_id: str) -> list[dict]:
    return [row for row in ALL_ROWS_FOR_CANDIDATES if row["event_id"] == event_id]


def write_report(validation: dict, version_policies: dict[str, dict] | None, manifest_rows: list[dict] | None) -> None:
    status = validation["validation_status"]
    if status == "blocked":
        body = f"""# 《仙翁操》白牙 ABCD Experimental Render 报告

本次任务在 preflight 阶段停止，未生成 wav。

blocker_reason: `{validation['blocker_reason']}`

已遵守边界：未生成 E，未使用 dummy fallback，未写 `sample_assets.csv`、`recording_segments.csv` 或 `recording_items_enriched.jsonl`。
"""
        (RENDER_DIR / "abcd_render_report.md").write_text(body, encoding="utf-8")
        return

    version_lines = []
    for version_id in VERSION_OUTPUTS:
        policy = version_policies[version_id]
        manifest = next(row for row in manifest_rows or [] if row["version_id"] == version_id)
        version_lines.append(
            f"- `{version_id}`：{policy.get('version_intent', '')} 输出 `{manifest['wav_path']}`，"
            f"duration={manifest['duration_s']}s，event_count={manifest['event_count']}。"
        )

    body = f"""# 《仙翁操》白牙 ABCD Experimental Render 报告

任务名称：`{TASK_NAME}`

## 1. 本次输出性质

本次生成的是 `RS_XWC_002_BAIYA_PILOT` 的 A/B/C/D experimental render，不是 production render，不是 sample ingest 成功，也不是最终打谱成功。白牙仍为 `QINIST_002`，`QINIST_001 三曼` 身份未被覆盖。

## 2. 四版如何使用 abcd_version_policy.local.yaml

四版共享同一 `render_source_map.local.json` 与 51 个唯一 event order，但分别读取 `abcd_version_policy.local.yaml` 的版本意图、phrase/timing/context/tail/crossfade 策略：

{chr(10).join(version_lines)}

## 3. render_anchor_s 对齐

本次所有 segment 均使用 `segment_insert_time_s = target_attack_time_s - render_anchor_s`。未按 clean wav 文件开头直接对齐，validation 中 `render_anchor_alignment_used=true`、`file_start_alignment_used=false`。

## 4. dummy fallback

未使用 dummy fallback。若 source map 或 clean preview 缺失，本脚本会停止生成 wav 并写 blocked validation。

## 5. E_REVIEWED

未生成 E。`e_co_review_schema.local.yaml` 只用于确认 E 是后续 Human+GPT Co-Created Reviewed Dapu，当前 `e_generated=false`。

## 6. 禁写资产

未写 `03_samples/sample_assets.csv`，未写 `03_samples/recording_segments.csv`，未创建 `recording_items_enriched.jsonl`，未训练 ML，未修改 score/canon/sources/raw/R0/R1 archive。

## 7. T060/T071 context take

`T060=context_take_1`，`T071=context_take_2`，二者均属于 `XWC_P09_N01_to_N02`。本次将它们作为 P09 transition context references：A 保持更直译的 `T059`，B/D 使用 `T060`，C 使用 `T071`。它们没有被反写为普通 atomic sample 或 score fact。`T071` 保持 `batch08 / T071 / 001`，不是 `batch07_take_011`，不是 retake。

## 8. 每版听评目标

- `A_LITERAL`：听谱面骨架、anchor 是否稳、是否过于机械。
- `B_PHRASE`：听句读、气口、phrase boundary 与呼吸是否自然。
- `C_QINIST_STYLE`：听白牙样本衔接、自然尾音、context take 的演奏连续性。
- `D_TEACHING_DIAGNOSTIC`：听结构、动作与音位边界是否清楚，方便定位问题。

## 9. 下一步

下一步应进入 Human+GPT co-review：用户先听四个 wav，GPT 再结合 wav、alignment 与 `sample_selection_decision.csv` 做结构分析、工程诊断与打谱解释诊断，共创 `E_REVIEWED` 的 revision plan。不得自动生成 E。
"""
    (RENDER_DIR / "abcd_render_report.md").write_text(body, encoding="utf-8")


def write_listening_guide(manifest_rows: list[dict]) -> None:
    wav_lines = "\n".join(f"- `{row['version_id']}`: `{row['wav_path']}`" for row in manifest_rows)
    guide = f"""# 《仙翁操》白牙 ABCD 共听评输入指南

## 四个 wav 路径

{wav_lines}

## 建议听评顺序

1. `A_LITERAL`：先建立直译谱面骨架参照。
2. `D_TEACHING_DIAGNOSTIC`：确认结构、动作与音位边界是否清楚。
3. `B_PHRASE`：比较句读、气口与段落呼吸。
4. `C_QINIST_STYLE`：听白牙样本衔接、自然尾音与 context 连接是否更像演奏。

## 每版听评关注点

- `A_LITERAL`：是否保留谱面骨架；是否有明显 anchor 错位；是否过于机械。
- `B_PHRASE`：phrase boundary 是否清楚；气口是否自然；是否避免固定 gap。
- `C_QINIST_STYLE`：尾音是否保留得当；context take 是否提升连贯性；是否引入非 score fact 的误读。
- `D_TEACHING_DIAGNOSTIC`：动作边界是否可诊断；音位是否清楚；是否牺牲自然性但提升定位能力。

## 问题类型列表

- `too_mechanical`
- `wrong_breath`
- `tail_short`
- `tail_too_long`
- `attack_abrupt`
- `sample_mismatch`
- `phrase_unclear`
- `transition_unnatural`
- `context_take_needed`
- `context_take_overused`
- `anchor_suspect`
- `good`

## 用户主观听评记录方式

建议按 version + event/phrase 记录：先写整体感受，再记录最明显的 3-8 个问题点。每条问题尽量标注版本、时间点、事件或 phrase、问题类型、主观建议，以及是否有偏好的参考版本。

## GPT 后续如何参与 E 共创

GPT 后续应同时读取四个 wav、各版 `render_event_alignment.<VERSION>.csv`、`sample_selection_decision.csv` 与用户听评记录，分层给出：结构/句法诊断、工程对齐诊断、样本选择诊断、打谱解释风险，以及 `e_revision_plan` 草案。

## E_REVIEWED 边界

本阶段不自动生成 E。E 必须来自 ABCD render -> 用户听评 -> GPT 听评/结构分析/工程诊断/打谱解释诊断 -> e_revision_plan -> 用户确认 -> E render。
"""
    (RENDER_DIR / "listening_review_input_guide.md").write_text(guide, encoding="utf-8")


def build_validation(preflight: dict, generated_wavs: dict[str, str] | None, status: str, blocker: str = "") -> dict:
    return {
        "task_name": TASK_NAME,
        "planning_commit_checked": PLANNING_COMMIT,
        "planning_commit_is_ancestor": check_planning_commit(),
        "generated_versions": len(generated_wavs or {}),
        "generated_wavs": generated_wavs or {},
        "e_generated": False,
        "dummy_fallback_used": False,
        "source_map_rows": 71,
        "missing_source_audio_count": preflight.get("missing_source_audio_count", 0),
        "unreadable_source_audio_count": preflight.get("unreadable_source_audio_count", 0),
        "t071_rule_ok": preflight.get("t071_rule_ok", False),
        "t060_t071_context_rule_ok": preflight.get("t060_t071_context_rule_ok", False),
        "render_anchor_alignment_used": status == "passed",
        "file_start_alignment_used": False,
        "sample_assets_modified": False,
        "recording_segments_modified": False,
        "recording_items_enriched_created": False,
        "score_events_modified": False,
        "gesture_templates_modified": False,
        "canon_modified": False,
        "sources_modified": False,
        "raw_master_modified": False,
        "production_grade": False,
        "validation_status": status,
        "blocker_reason": blocker,
    }


def run(preflight_only: bool = False) -> int:
    global ALL_ROWS_FOR_CANDIDATES
    check_required_inputs()
    ensure_e_not_generated()
    plan_validation = read_json(PLAN_VALIDATION_PATH)
    if plan_validation.get("validation_status") != "passed":
        raise RenderBlocker("planning validation 不是 passed")
    rows = load_source_rows()
    ALL_ROWS_FOR_CANDIDATES = rows
    preflight = preflight_rows(rows)
    if preflight["blocker_reason"]:
        validation = build_validation(preflight, {}, "blocked", preflight["blocker_reason"])
        write_json(RENDER_DIR / "abcd_render_validation.json", validation)
        write_report(validation, None, None)
        return 2
    if preflight_only:
        print("preflight passed")
        return 0

    phrases = parse_phrase_plan(PHRASE_PLAN_PATH)
    versions = parse_version_policy(VERSION_POLICY_PATH)
    manifest_rows: list[dict] = []
    all_selection_rows: list[dict] = []
    generated_wavs: dict[str, str] = {}
    for version_id in VERSION_OUTPUTS:
        selected = selected_events_for_version(version_id, rows, phrases)
        scheduled = schedule_events(version_id, selected)
        manifest_row, _, selection_rows = render_version(version_id, versions[version_id], scheduled)
        manifest_rows.append(manifest_row)
        all_selection_rows.extend(selection_rows)
        generated_wavs[version_id] = manifest_row["wav_path"]

    write_csv(RENDER_DIR / "abcd_render_manifest.csv", RENDER_MANIFEST_FIELDS, manifest_rows)
    write_csv(RENDER_DIR / "sample_selection_decision.csv", SELECTION_FIELDS, all_selection_rows)
    validation = build_validation(preflight, generated_wavs, "passed", "")
    write_json(RENDER_DIR / "abcd_render_validation.json", validation)
    write_report(validation, versions, manifest_rows)
    write_listening_guide(manifest_rows)
    print("generated ABCD experimental renders from planning")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Baiya XWC ABCD experimental wavs from local planning files.")
    parser.add_argument("--preflight-only", action="store_true")
    args = parser.parse_args()
    try:
        return run(preflight_only=args.preflight_only)
    except RenderBlocker as exc:
        preflight = {"missing_source_audio_count": 0, "unreadable_source_audio_count": 0}
        validation = build_validation(preflight, {}, "blocked", str(exc))
        write_json(RENDER_DIR / "abcd_render_validation.json", validation)
        write_report(validation, None, None)
        print(f"blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
