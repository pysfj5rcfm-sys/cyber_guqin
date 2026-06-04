#!/usr/bin/env python3
"""Validate Phase S0 Dapu Event IR minimal fixture."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "xianwengcao_events_minimal.jsonl"
REPORT = ROOT / "reports" / "validate_dapu_ir_report.json"

ALLOWED_SOUND_TYPES = {"散音", "按音", "泛音"}
ALLOWED_COMPONENT_SOUND_TYPES = {"散音", "按音", "泛音", "none"}
ALLOWED_PRE_ACTIONS = {"none", "chuo", "zhu"}
ALLOWED_VIBRATO = {"none", "yin", "nao", "yin_nao"}


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no} invalid JSON: {exc}")
            continue
        if not isinstance(value, dict):
            errors.append(f"line {line_no} must be a JSON object")
            continue
        rows.append(value)
    return rows


def component_categories(event: dict[str, Any], name: str) -> list[str]:
    return [
        comp.get("component_category")
        for comp in event.get("components", [])
        if isinstance(comp, dict) and comp.get("component_name") == name
    ]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    rows = load_jsonl(FIXTURE, errors) if FIXTURE.exists() else []
    if not FIXTURE.exists():
        errors.append(f"missing fixture {FIXTURE}")

    by_id = {row.get("event_id"): row for row in rows}

    for row in rows:
        event_id = row.get("event_id", "<missing>")
        add(errors, bool(row.get("event_id")), "event missing event_id")
        add(errors, row.get("primary_sound_type") in ALLOWED_SOUND_TYPES, f"{event_id} invalid primary_sound_type")
        add(errors, bool(row.get("gesture_family")), f"{event_id} missing gesture_family")
        components = row.get("components")
        add(errors, isinstance(components, list) and bool(components), f"{event_id} missing components")
        add(errors, not (row.get("source_status") == "ocr_candidate" and row.get("needs_review") is not True), f"{event_id} OCR candidate must need review")
        add(errors, row.get("notation_pre_action") in ALLOWED_PRE_ACTIONS, f"{event_id} invalid notation_pre_action")
        add(errors, row.get("notation_vibrato") in ALLOWED_VIBRATO, f"{event_id} invalid notation_vibrato")
        add(errors, not (row.get("source_status") == "ocr_candidate" and row.get("source_status") == "verified"), f"{event_id} OCR candidate cannot be verified")
        if isinstance(components, list):
            for comp in components:
                if not isinstance(comp, dict):
                    errors.append(f"{event_id} component must be object")
                    continue
                add(errors, comp.get("component_sound_type") in ALLOWED_COMPONENT_SOUND_TYPES, f"{event_id} component {comp.get('component_name')} invalid component_sound_type")
                add(errors, "percussive" not in comp, f"{event_id} must not use percussive field")
        if row.get("notation_pre_action") == "chuo" and "绰" not in str(row.get("source_token", "")):
            errors.append(f"{event_id} default chuo must not auto-enter event")
        if "注" in str(row.get("source_token", "")):
            add(errors, row.get("notation_pre_action") == "zhu", f"{event_id} explicit 注 must map to notation_pre_action=zhu")

    zhuang_event = by_id.get("AN_THUMB_9_GOU_4_ZHUANG", {})
    add(errors, "micro_returning_slide" in component_categories(zhuang_event, "zhuang"), "撞 must be micro_returning_slide")

    qiaqi_event = by_id.get("AN_RING_10_QIAQI", {})
    add(errors, qiaqi_event.get("gesture_family") == "left_hand_sound", "掐起 event must be left_hand_sound")

    cuo_event = by_id.get("FAN_DA7_ZHONG7_CUO_6_1", {})
    add(errors, cuo_event.get("gesture_family") == "simultaneous_pluck", "撮 event must be simultaneous_pluck")

    for event_id, row in by_id.items():
        if "分开" in str(row.get("source_token", "")):
            add(errors, row.get("gesture_family") != "open_pressed_harmony", f"{event_id} 分开 must not be open_pressed_harmony")

    expected_ids = {
        "SAN_TIAO_7",
        "AN_RING_10_GOU_5",
        "AN_RING_10_8_GOU_3",
        "AN_THUMB_9_GOU_6_SHANG_79",
        "AN_THUMB_9_GOU_4_ZHUANG",
        "AN_RING_10_QIAQI",
        "FAN_DA7_ZHONG7_CUO_6_1",
    }
    missing = sorted(expected_ids - set(by_id))
    add(errors, not missing, f"missing expected event ids: {missing}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "validator": "validate_dapu_ir.py",
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": {"events": len(rows)},
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
