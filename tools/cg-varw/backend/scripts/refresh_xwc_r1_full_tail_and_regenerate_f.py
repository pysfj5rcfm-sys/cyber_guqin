from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import sys
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services import r2_mock_store as r2_store  # noqa: E402
import generate_xwc_f_final_reviewed as f_generator  # noqa: E402


RENDER_ROOT = REPO_ROOT / "04_outputs" / "XWC" / "RS_XWC_002_BAIYA_PILOT" / "abcd_experimental_render"
SESSION_ROOT = REPO_ROOT / "02_recordings" / "raw_audio" / "QINIST_002" / "XWC" / "RS_XWC_002_BAIYA_PILOT"
SPLIT_ROOT = SESSION_ROOT / "split_preview"
R1_ARCHIVE_ROOT = SESSION_ROOT / "r1_review"
R1_WORKBENCH_ROOT = REPO_ROOT / "tools" / "cg-varw" / "review_outputs" / "r1"
F_DIR = RENDER_ROOT / "F_FINAL_REVIEWED"
F_ARCHIVE_DIR = RENDER_ROOT / "F_FINAL_REVIEWED_BEFORE_FULL_TAIL_FIX"
LATEST_DIR = RENDER_ROOT / "r2_review_drafts" / "latest"
LATEST_STATE = LATEST_DIR / "r2_review_state.latest.json"
DOC_REPORT = REPO_ROOT / "tools" / "cg-varw" / "docs" / "CG_VARW_R1_FULL_TAIL_REFRESH_AND_F_REGEN_REPORT_v0.1.md"
RENDER_SET_ID = "R2_XWC_BAIYA_ABCD_EXPERIMENTAL_354811e"


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    os.environ["CG_VARW_R2_RENDER_ROOT"] = str(RENDER_ROOT)
    os.environ["CG_VARW_R2_INTAKE_ROOT"] = str(RENDER_ROOT / "r2_review_intake")

    audit_before = audit_r1_and_f()
    archive_info = archive_old_f()
    preview_rows = regenerate_full_tail_previews(generated_at)
    r1_policy = refresh_r1_tail_policy(generated_at)

    f_result = f_generator.main()
    if f_result != 0:
        return f_result

    state = read_json(LATEST_STATE)
    new_f_wav = F_DIR / "XWC_BAIYA_F_FINAL_REVIEWED.wav"
    validation = read_json(F_DIR / "f_final_validation.json")
    refresh_metadata = {
        "schema_id": "CG_VARW_R1_FULL_TAIL_REFRESH_v0.1",
        "generated_at": generated_at,
        "old_f_archive": archive_info,
        "new_f_sha256": sha256(new_f_wav),
        "new_f_wav_metadata": wav_meta(new_f_wav),
        "new_f_tempo_ratio": validation.get("tempo_ratio"),
        "r1_policy": r1_policy,
        "preview_refresh": summarize_preview_refresh(preview_rows),
        "unresolved_tail_recovery": [row for row in preview_rows if row["tail_recovery_unavailable"] == "true"],
    }
    state["f_full_tail_refresh"] = refresh_metadata
    state["f_tail_policy"] = "full_tail"
    state["f_tail_refresh_completed"] = True
    state["f_tail_refresh_source"] = "R1_FULL_TAIL_PREVIEW_REFRESH"
    state["saved_at"] = generated_at
    write_json(LATEST_STATE, state)
    export_tables = r2_store.export_tables_from_canonical_state(RENDER_SET_ID, state)
    files = r2_store.write_export_tables(LATEST_DIR, export_tables)
    r2_store.write_review_state_manifest(LATEST_DIR, state, files, LATEST_DIR)

    write_csv(F_DIR / "full_tail_preview_refresh_manifest.csv", preview_rows)
    write_json(F_DIR / "full_tail_refresh_audit.json", {"before": audit_before, "after": refresh_metadata})
    write_report(audit_before, refresh_metadata, validation)
    print(json.dumps({"ok": True, "archive": str(F_ARCHIVE_DIR), "new_f": str(new_f_wav), "preview_rows": len(preview_rows)}, ensure_ascii=False, indent=2))
    return 0


def audit_r1_and_f() -> dict[str, Any]:
    f_alignment = read_csv(F_DIR / "render_event_alignment.F_FINAL_REVIEWED.csv")
    f_sources = sorted({row.get("source_take_id", "") for row in f_alignment if row.get("source_take_id")})
    likely_tail_cut_events = [
        row["event_id"]
        for row in f_alignment
        if row.get("event_id", "").endswith(("N04", "N06", "N07"))
        or abs(float(row.get("target_attack_time_s", "0")) - float(row.get("phrase_play_end_s", "0"))) < 2.5
    ]
    registry_rows = read_all_r1_anchor_rows()
    smart_fade_rows = [row for row in registry_rows if row.get("tail_policy") == "smart_fade_100ms"]
    full_tail_rows = [row for row in registry_rows if row.get("tail_policy") == "full_tail"]
    missing_tail = [row.get("take_id", "") for row in registry_rows if not row.get("tail_end_s")]
    return {
        "f_source_count": len(f_sources),
        "f_source_take_ids": f_sources,
        "f_current_source_from_clean_previews": all("clean_previews" in row.get("source_audio", "") for row in f_alignment),
        "f_current_plan_uses_smart_fade": "safe_trim_smart_fade: true" in (F_DIR / "f_revision_plan.yaml").read_text(encoding="utf-8"),
        "f_safe_trimmed_event_count": read_json(F_DIR / "f_final_validation.json").get("wav_metadata", {}).get("safe_trimmed_event_count"),
        "r1_registry_rows": len(registry_rows),
        "r1_smart_fade_count": len(smart_fade_rows),
        "r1_full_tail_count": len(full_tail_rows),
        "r1_missing_tail_end_take_ids": missing_tail,
        "f_likely_tail_cut_events": likely_tail_cut_events,
    }


def archive_old_f() -> dict[str, Any]:
    if not F_DIR.exists():
        raise SystemExit(f"missing F dir: {F_DIR}")
    if F_ARCHIVE_DIR.exists():
        metadata = F_ARCHIVE_DIR / "archive_metadata.json"
        if metadata.exists():
            return read_json(metadata)
        raise SystemExit(f"archive already exists without metadata, refusing to overwrite: {F_ARCHIVE_DIR}")
    shutil.copytree(F_DIR, F_ARCHIVE_DIR)
    wav_path = F_ARCHIVE_DIR / "XWC_BAIYA_F_FINAL_REVIEWED.wav"
    validation_path = F_ARCHIVE_DIR / "f_final_validation.json"
    validation = read_json(validation_path) if validation_path.exists() else {}
    info = {
        "archive_path": str(F_ARCHIVE_DIR),
        "old_f_sha256": sha256(wav_path),
        "old_f_wav_metadata": wav_meta(wav_path),
        "old_f_tempo_ratio": validation.get("tempo_ratio") or validation.get("wav_metadata", {}).get("tempo_ratio"),
    }
    write_json(F_ARCHIVE_DIR / "archive_metadata.json", info)
    return info


def regenerate_full_tail_previews(generated_at: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for manifest_path in sorted(SPLIT_ROOT.glob("batch*/manifests/recd2_split_preview_manifest.csv")):
        for item in read_csv(manifest_path):
            take_id = item["recording_take_no"]
            raw_path = REPO_ROOT / item["source_raw_audio"]
            clean_path = REPO_ROOT / item["clean_preview_audio"]
            unit_path = REPO_ROOT / item["unit_preview_audio"]
            clean_start = parse_float(item.get("clean_start_s"))
            clean_end = parse_float(item.get("clean_end_s") or item.get("tail_end_s"))
            unit_start = parse_float(item.get("unit_start_s"))
            unit_end = parse_float(item.get("unit_end_s") or item.get("tail_end_s"))
            unresolved = not raw_path.exists() or clean_start is None or clean_end is None or clean_end <= clean_start
            old_clean_hash = sha256(clean_path) if clean_path.exists() else ""
            old_unit_hash = sha256(unit_path) if unit_path.exists() else ""
            if not unresolved:
                slice_wav(raw_path, clean_path, clean_start, clean_end)
                if unit_start is not None and unit_end is not None and unit_end > unit_start:
                    slice_wav(raw_path, unit_path, unit_start, unit_end)
            new_clean_hash = sha256(clean_path) if clean_path.exists() else ""
            new_unit_hash = sha256(unit_path) if unit_path.exists() else ""
            rows.append(
                {
                    "generated_at": generated_at,
                    "batch_id": item["batch_id"],
                    "take_id": take_id,
                    "event_id": item["event_id"],
                    "source_raw_audio": item["source_raw_audio"],
                    "clean_preview_audio": item["clean_preview_audio"],
                    "unit_preview_audio": item["unit_preview_audio"],
                    "tail_policy": "full_tail",
                    "tail_end_s": item.get("tail_end_s") or item.get("clean_end_s") or "",
                    "tail_duration_s": f"{(clean_end - clean_start):.6f}" if clean_start is not None and clean_end is not None else "",
                    "regenerated_from_raw": "false" if unresolved else "true",
                    "tail_recovery_unavailable": "true" if unresolved else "false",
                    "clean_preview_old_sha256": old_clean_hash,
                    "clean_preview_new_sha256": new_clean_hash,
                    "clean_preview_changed": "true" if old_clean_hash and old_clean_hash != new_clean_hash else "false",
                    "unit_preview_old_sha256": old_unit_hash,
                    "unit_preview_new_sha256": new_unit_hash,
                    "unit_preview_changed": "true" if old_unit_hash and old_unit_hash != new_unit_hash else "false",
                }
            )
    return rows


def refresh_r1_tail_policy(generated_at: str) -> dict[str, Any]:
    changed_files: list[str] = []
    changed_rows = 0
    for path in sorted(R1_ARCHIVE_ROOT.glob("batch*/reviewed_render_anchors*.csv")) + sorted(R1_WORKBENCH_ROOT.glob("exports/batch*/reviewed_render_anchors.csv")):
        rows = read_csv(path)
        for row in rows:
            if row.get("tail_policy") != "full_tail":
                row["tail_policy"] = "full_tail"
                changed_rows += 1
        write_csv(path, rows)
        changed_files.append(str(path))
    for path in sorted(R1_WORKBENCH_ROOT.glob("drafts/*.split_review.json")):
        data = read_json(path)
        changed = set_tail_policy_recursive(data)
        if changed:
            write_json(path, data)
            changed_files.append(str(path))
    return {
        "generated_at": generated_at,
        "tail_policy": "full_tail",
        "changed_rows": changed_rows,
        "changed_files": changed_files,
        "tracked_r1_archive_files": len(list(R1_ARCHIVE_ROOT.glob("batch*/reviewed_render_anchors*.csv"))),
    }


def write_report(audit_before: dict[str, Any], refresh: dict[str, Any], validation: dict[str, Any]) -> None:
    old_meta = refresh["old_f_archive"]["old_f_wav_metadata"]
    new_meta = refresh["new_f_wav_metadata"]
    unresolved = refresh["unresolved_tail_recovery"]
    report = f"""# CG-VARW R1 full_tail 刷新与 F_FINAL_REVIEWED 复生成报告 v0.1

## 结论

本任务将白牙 `RS_XWC_002_BAIYA_PILOT` 的 R1 注册 tail policy 从 `smart_fade_100ms` 刷新为 `full_tail`，从 raw/split manifest 重新写出 T-previewer 音频，并在不新增 G/F2 的前提下复生成同名 `F_FINAL_REVIEWED`。

## 为什么改为 full_tail

用户验收指出旧 F 基本通过，但尾音存在截断感。古琴尾音轻、长，和下一个音自然叠合时不一定造成明显堆叠，因此本轮不再以 smart fade 作为主要尾音策略；只保留自然衰减，允许轻尾自然混合。

## R1 刷新范围

- R1 注册范围：T001-T071。
- 刷新前 R1 registry `smart_fade_100ms` 行数：{audit_before['r1_smart_fade_count']}。
- 刷新后目标 tail_policy：`full_tail`。
- R1 changed_rows：{refresh['r1_policy']['changed_rows']}。
- T008：F source 仍不使用 T008；`XWC_P02_N03` 继续使用 T014。
- full_tail preview：{refresh['preview_refresh']['regenerated_from_raw_count']} 个 preview 从 raw/split manifest 重新写出。
- 无法恢复完整 tail：{len(unresolved)}。

## 旧 F 归档

- 归档路径：`{refresh['old_f_archive']['archive_path']}`
- 旧 F sha256：`{refresh['old_f_archive']['old_f_sha256']}`
- 旧 F 时长：{old_meta['duration_s']:.6f}s
- 旧 F tempo ratio：{refresh['old_f_archive']['old_f_tempo_ratio']}

## 新 F

- 新 F sha256：`{refresh['new_f_sha256']}`
- 新 F wav：{new_meta['duration_s']:.6f}s，{new_meta['sample_rate_hz']} Hz，{new_meta['bit_depth']} bit。
- 新 F tempo ratio：{refresh['new_f_tempo_ratio']}
- 新 F 仍保持原 F attack timeline 与约 1.5 倍速策略，只将 source preview / tail policy 切换为 full_tail。
- P01/P06-P09 仍为 N03->N04；P02-P05 仍为 N05->N06。
- P02_N03：{validation.get('p02_n03_source_take_id')}。
- source_take_id 不含 T008：{validation.get('t008_exclusion')}.
- smart_fade_applied：{validation.get('smart_fade_applied')}.
- tail_trimmed_event_count：{validation.get('tail_trimmed_event_count')}.

## R2 与导出同步

- R2 版本仍为 A/B/C/D/E/F，不新增 G/F2。
- `preferredVersionByPhrase` 仍为 F。
- `render_phrase_alignment.csv`：{validation.get('render_phrase_alignment_rows')} 行。
- `phrase_boundary_decision.csv`：{validation.get('phrase_boundary_decision_rows')} 行。
- 8 个 CSV/YAML 从 canonical latest state 重新派生。
- 未恢复 Downloads、Blob 或 `a.download`。
- 未修改 R2 按钮。
- 未重做 A/B/C/D/E。

## R0 遗留问题

`LEGACY_R0_DRAFT_LOAD_NOT_VERIFIED`：用户已验证 R0 仍未加载出口播标记。本任务不处理 R0；F full_tail 修复后再单独开 R0 recovery/audit。

## 用户验收

请打开 R2，选择 `F_FINAL_REVIEWED`，重点听 P01/P06-P09 的 N03->N04、P02-P05 的 N05->N06，以及每句 cadence/final note 的自然尾音。预期是节奏与旧 F 一致，但尾音不再有明显截断。
"""
    DOC_REPORT.write_text(report, encoding="utf-8")


def summarize_preview_refresh(rows: list[dict[str, str]]) -> dict[str, Any]:
    return {
        "row_count": len(rows),
        "regenerated_from_raw_count": sum(1 for row in rows if row["regenerated_from_raw"] == "true"),
        "clean_preview_changed_count": sum(1 for row in rows if row["clean_preview_changed"] == "true"),
        "unit_preview_changed_count": sum(1 for row in rows if row["unit_preview_changed"] == "true"),
        "tail_recovery_unavailable_count": sum(1 for row in rows if row["tail_recovery_unavailable"] == "true"),
    }


def slice_wav(source: Path, dest: Path, start_s: float, end_s: float) -> None:
    with wave.open(str(source), "rb") as src:
        params = src.getparams()
        sample_rate = src.getframerate()
        start_frame = max(0, int(round(start_s * sample_rate)))
        end_frame = min(src.getnframes(), int(round(end_s * sample_rate)))
        src.setpos(start_frame)
        frames = src.readframes(max(0, end_frame - start_frame))
    dest.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(dest), "wb") as out:
        out.setparams(params)
        out.writeframes(frames)


def read_all_r1_anchor_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(R1_ARCHIVE_ROOT.glob("batch*/reviewed_render_anchors*.csv")):
        rows.extend(read_csv(path))
    return rows


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def set_tail_policy_recursive(value: Any) -> bool:
    changed = False
    if isinstance(value, dict):
        if value.get("tail_policy") is not None and value.get("tail_policy") != "full_tail":
            value["tail_policy"] = "full_tail"
            changed = True
        for item in value.values():
            changed = set_tail_policy_recursive(item) or changed
    elif isinstance(value, list):
        for item in value:
            changed = set_tail_policy_recursive(item) or changed
    return changed


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


if __name__ == "__main__":
    raise SystemExit(main())
