#!/usr/bin/env python3
"""Export human-readable recording checklists for Phase 1A."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIECE_DIR = ROOT / "01_pieces" / "xianwengcao"
GLOBAL_DIR = ROOT / "00_global"

RECORDING_SCRIPT = PIECE_DIR / "recording_script.csv"
SCORE_EVENTS = PIECE_DIR / "score_events.csv"
GESTURE_TEMPLATES = GLOBAL_DIR / "gesture_templates.csv"
GESTURE_COMPONENTS = GLOBAL_DIR / "gesture_components.csv"

HUMAN_CSV = PIECE_DIR / "recording_script_human.csv"
HUMAN_MD = PIECE_DIR / "recording_script_human.md"
BATCHES_MD = PIECE_DIR / "recording_batches.md"

OUTPUT_FIELDS = [
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
    "recommended_pause_s",
    "need_full_decay",
    "human_instruction",
    "notes",
]

BATCH_ORDER = [
    "散音 straight",
    "泛音 straight",
    "普通按音 straight",
    "普通按音 chuo",
    "明示注 zhu",
    "特殊/context",
    "复合泛音/撮",
]

FINGER_NAMES = {
    "ring": "名指",
    "thumb": "大指",
    "index": "食指",
    "middle": "中指",
}

ACTION_NAMES = {
    "gou": "勾",
    "tiao": "挑",
    "bo": "擘",
    "cuo": "撮",
}

NUMERAL_NAMES = {
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
    "10": "十",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def index_by(rows: list[dict[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows if row.get(key)}


def components_by_gesture(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["gesture_id"]].append(row)
    for gesture_rows in grouped.values():
        gesture_rows.sort(key=lambda r: int(r.get("component_order") or 0))
    return grouped


def pause_phrase(row: dict[str, str]) -> str:
    pause = row.get("recommended_pause_s") or "1.5"
    return f"结束后停 {pause} 秒。"


def decay_phrase(row: dict[str, str]) -> str:
    return "保留余音，" if row.get("need_full_decay", "").lower() == "true" else ""


def hui_label(value: str) -> str:
    if not value:
        return ""
    parts = value.split(".")
    major = NUMERAL_NAMES.get(parts[0], parts[0])
    if len(parts) == 1:
        return f"{major}徽"
    minor = NUMERAL_NAMES.get(parts[1], parts[1])
    return f"{major}徽{minor}"


def string_label(value: str) -> str:
    if "+" in value:
        return "".join(NUMERAL_NAMES.get(part, part) for part in value.split("+"))
    return NUMERAL_NAMES.get(value, value)


def event_display_name(event_id: str, events: dict[str, dict[str, str]]) -> str:
    event = events.get(event_id, {})
    if event_id == "XWC_P09_N01":
        return "大注九勾四撞"
    return event.get("normalized_input") or event.get("normalized_name") or ""


def event_label(event_id: str, events: dict[str, dict[str, str]]) -> str:
    name = event_display_name(event_id, events)
    return f"{event_id} {name}".strip()


def take_note(row: dict[str, str]) -> str:
    script_id = row.get("script_id", "")
    if script_id == "RS_XWC_001_060":
        return "掐起 context take 1"
    if script_id == "RS_XWC_001_071":
        return "撞到掐起 context take 2 / event_range 正式上下文"
    return ""


def context_instruction(row: dict[str, str], events: dict[str, dict[str, str]]) -> str:
    event_id = row.get("event_id", "")
    current = event_label(event_id, events)
    previous_id = ""

    if row.get("event_range") == "XWC_P09_N01_to_N02" or event_id == "XWC_P09_N02":
        previous_id = "XWC_P09_N01"
    else:
        event = events.get(event_id, {})
        previous_id = event.get("inherited_from_event_id") or ""
        if not previous_id and row.get("event_range"):
            previous_id = row["event_range"].split("_to_")[0]

    if previous_id == "XWC_P09_N01":
        return (
            f"录上下文版本：从 {event_label(previous_id, events)} 接到 {current}，"
            "重点保持‘注—勾四—撞—掐起’的承接自然。"
            "撞要小幅、落点偏虚；掐起不要像孤立插入音。"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )

    if previous_id:
        return (
            f"录上下文版本：从 {event_label(previous_id, events)} 接到 {current}，"
            f"重点保持前一声到{row['normalized_name']}的承接自然，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    return (
        f"录{row['normalized_name']}的上下文版本，保留前后动作的自然气口，"
        f"{decay_phrase(row)}{pause_phrase(row)}"
    )


def san_instruction(row: dict[str, str], template: dict[str, str]) -> str:
    action = ACTION_NAMES.get(template.get("primary_right_action", ""), "")
    string_no = string_label(template.get("primary_string_no", ""))
    return f"弹散音{action}{string_no}弦，{decay_phrase(row)}{pause_phrase(row)}"


def fan_instruction(row: dict[str, str], template: dict[str, str]) -> str:
    name = row["normalized_name"]
    if template.get("is_composite") == "true" or "撮" in name:
        return (
            f"录复合泛音{name}，两声同时起，手法保持干净，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    return f"录泛音{name}，泛音点轻触清楚，{decay_phrase(row)}{pause_phrase(row)}"


def post_motion_instruction(row: dict[str, str], template: dict[str, str]) -> str:
    name = row["normalized_name"]
    variant = row.get("realization_variant", "")
    finger = FINGER_NAMES.get(template.get("primary_left_finger", ""), "")
    hui = hui_label(template.get("primary_hui", ""))
    action = ACTION_NAMES.get(template.get("primary_right_action", ""), "")
    string_no = string_label(template.get("primary_string_no", ""))

    if row.get("gesture_id") == "AN_THUMB_9_GOU_6_SHANG_79":
        if variant == "chuo":
            return (
                "大指九徽勾六弦，按三曼习惯加入自然绰音；"
                "勾六出声后上滑至七徽九分。"
                f"绰不要夸张，上滑要拖开，保留滑音过程和余音，{pause_phrase(row)}"
            )
        return (
            "大指按九徽，勾六弦出声后上滑至七徽九分；"
            "直按版本，不主动加绰。"
            f"上滑要拖开，保留滑音过程和余音，{pause_phrase(row)}"
        )

    base = f"{finger}{hui}{action}{string_no}弦"
    if "撞" in name and variant == "zhu":
        return (
            f"{base}，录注按并带撞版本；撞为小幅回返，落点偏虚，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    if "撞" in name:
        return (
            f"{base}，带撞动作，撞幅度小，不要压重，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    return (
        f"{base}，录谱面明示的走手版本，过程要听得见，"
        f"{decay_phrase(row)}{pause_phrase(row)}"
    )


def pressed_instruction(row: dict[str, str], template: dict[str, str]) -> str:
    name = row["normalized_name"]
    variant = row.get("realization_variant", "")
    finger = FINGER_NAMES.get(template.get("primary_left_finger", ""), "")
    hui = hui_label(template.get("primary_hui", ""))
    action = ACTION_NAMES.get(template.get("primary_right_action", ""), "")
    string_no = string_label(template.get("primary_string_no", ""))
    base = f"{finger}{hui}{action}{string_no}弦"

    if template.get("sound_profile") == "post_motion" or template.get("gesture_family") == "post_motion":
        return post_motion_instruction(row, template)
    if variant == "zhu":
        return (
            f"{base}，录注按版本，注为谱面明示动作，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    if variant == "chuo":
        return (
            f"{base}，按三曼习惯加入自然绰音，注意绰不要夸张，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    if variant == "atomic":
        return (
            f"单独录{name}，动作放清楚，保留左手发音的自然起点，"
            f"{decay_phrase(row)}{pause_phrase(row)}"
        )
    return (
        f"{finger}按{hui}，{action}{string_no}弦，直按版本，"
        f"不主动加绰，{decay_phrase(row)}{pause_phrase(row)}"
    )


def human_instruction(
    row: dict[str, str],
    templates: dict[str, dict[str, str]],
    events: dict[str, dict[str, str]],
) -> str:
    if row.get("expected_sample_type") == "context" or row.get("realization_variant") == "context":
        return context_instruction(row, events)

    template = templates.get(row["gesture_id"], {})
    sound_type = template.get("primary_sound_type", "")
    if sound_type == "散音":
        return san_instruction(row, template)
    if sound_type == "泛音":
        return fan_instruction(row, template)
    if sound_type == "按音":
        return pressed_instruction(row, template)
    return f"录{row['normalized_name']}，{decay_phrase(row)}{pause_phrase(row)}"


def batch_name(row: dict[str, str], template: dict[str, str]) -> str:
    variant = row.get("realization_variant", "")
    sound_type = template.get("primary_sound_type", "")
    if row.get("expected_sample_type") == "context" or variant in {"context", "atomic"}:
        return "特殊/context"
    if template.get("is_composite") == "true" and sound_type == "泛音":
        return "复合泛音/撮"
    if sound_type == "散音" and variant == "straight":
        return "散音 straight"
    if sound_type == "泛音" and variant == "straight":
        return "泛音 straight"
    if variant == "zhu":
        return "明示注 zhu"
    if sound_type == "按音" and variant == "chuo":
        return "普通按音 chuo"
    if sound_type == "按音" and variant == "straight":
        return "普通按音 straight"
    return "特殊/context"


def md_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join((row.get(field, "") or "").replace("|", "/") for field in fields) + " |")
    return "\n".join([header, sep, *body])


def write_human_csv(rows: list[dict[str, str]]) -> None:
    HUMAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    with HUMAN_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_human_md(rows: list[dict[str, str]]) -> None:
    HUMAN_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 《仙翁操》真实录音清单（Phase 1A）",
        "",
        "用途：给琴人“三曼”录音当天逐条查看。此文件由 `recording_script.csv` 导出，不修改原始谱面、ontology 或 dummy render。",
        "",
        f"总任务数：{len(rows)}",
        "",
        md_table(rows, OUTPUT_FIELDS),
        "",
    ]
    HUMAN_MD.write_text("\n".join(lines), encoding="utf-8")


def write_batches_md(rows: list[dict[str, str]], batches: dict[str, list[dict[str, str]]]) -> None:
    BATCHES_MD.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 《仙翁操》录音批次建议（Phase 1A）",
        "",
        "## 全量录音建议",
        "",
        "- 可以按本文件批次顺序全量录制。",
        "- 这是采样顺序，不是原曲演奏顺序。",
        "- 建议每个批次单独录成一个 wav 文件。",
        "- 每条任务之间留 2–3 秒静音。",
        "- context 条目留 3–4 秒静音。",
        "- 现场录音时建议按 batch_take_no 顺序读号和弹奏；recording_take_no / order_no / script_id 用于工程追踪。",
        "- 若录成一个长文件，建议每条前轻声读 recording_take_no 或 script_id，便于后续切分。",
        "",
        "## 建议录音顺序",
        "",
        "1. 先录散音和泛音。",
        "2. 再录普通按音 straight。",
        "3. 再录普通按音 chuo。",
        "4. 再录明示注 zhu。",
        "5. 最后录特殊/context。",
        "",
        f"总任务数：{len(rows)}",
        "",
    ]
    batch_fields = [
        "batch_take_no",
        "recording_take_no",
        "order_no",
        "script_id",
        "event_id",
        "event_range",
        "normalized_name",
        "realization_variant",
        "human_instruction",
        "notes",
    ]
    for name in BATCH_ORDER:
        group = batches.get(name, [])
        lines.extend([f"## {name}", "", f"任务数：{len(group)}", ""])
        if group:
            lines.append(md_table(group, batch_fields))
            lines.append("")
        else:
            lines.append("_无_")
            lines.append("")
    BATCHES_MD.write_text("\n".join(lines), encoding="utf-8")


def merged_notes(row: dict[str, str]) -> str:
    note = row.get("notes", "")
    take = take_note(row)
    if not take:
        return note
    if not note:
        return take
    return f"{note}；{take}"


def assign_batch_take_numbers(batches: dict[str, list[dict[str, str]]]) -> None:
    take_no = 1
    for batch in BATCH_ORDER:
        for row in batches.get(batch, []):
            row["batch_take_no"] = f"{take_no:03d}"
            take_no += 1


def main() -> None:
    recording_rows = read_csv(RECORDING_SCRIPT)
    score_events = index_by(read_csv(SCORE_EVENTS), "event_id")
    templates = index_by(read_csv(GESTURE_TEMPLATES), "gesture_id")
    # Loaded to keep the Phase 1A export tied to the ontology component table.
    components_by_gesture(read_csv(GESTURE_COMPONENTS))

    human_rows = []
    batches: dict[str, list[dict[str, str]]] = defaultdict(list)

    for index, row in enumerate(recording_rows, start=1):
        template = templates.get(row["gesture_id"], {})
        out = {field: row.get(field, "") for field in OUTPUT_FIELDS if field not in {"batch_take_no", "recording_take_no", "human_instruction", "notes"}}
        out["batch_take_no"] = ""
        out["recording_take_no"] = f"{index:03d}"
        out["human_instruction"] = human_instruction(row, templates, score_events)
        out["notes"] = merged_notes(row)
        ordered = {field: out.get(field, "") for field in OUTPUT_FIELDS}
        human_rows.append(ordered)
        batches[batch_name(row, template)].append(ordered)

    assign_batch_take_numbers(batches)
    write_human_csv(human_rows)
    write_human_md(human_rows)
    write_batches_md(human_rows, batches)

    print(f"Wrote {HUMAN_CSV.relative_to(ROOT)}")
    print(f"Wrote {HUMAN_MD.relative_to(ROOT)}")
    print(f"Wrote {BATCHES_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
