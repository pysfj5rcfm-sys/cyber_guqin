#!/usr/bin/env python3
"""Validate Phase S0 canon minimal fixture without third-party requirements."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "canon_minimal.yaml"
REPORT = ROOT / "reports" / "validate_canon_report.json"

ALLOWED_SOUND_TYPES = {"散音", "按音", "泛音", "none"}
ALLOWED_GESTURE_FAMILIES = {
    "single_pluck",
    "pressed_pluck",
    "harmonic_pluck",
    "simultaneous_pluck",
    "right_hand_sequence",
    "left_hand_sound",
    "post_motion",
    "vibrato",
    "open_pressed_harmony",
    "compound_both_hands",
    "tempo_expression",
}
REQUIRED_COMPONENT_FIELDS = {
    "component_name",
    "zh_name",
    "component_category",
    "hand",
    "standard_internal_name",
    "aliases",
    "description",
    "source_refs",
    "review_status",
    "confidence",
}
REQUIRED_TECHNIQUE_FIELDS = {
    "technique_id",
    "name_zh",
    "category",
    "definition",
    "primary_sound_type",
    "sound_profile",
    "gesture_family",
    "component_rules",
    "cyber_guqin_mapping",
    "source_refs",
    "review_status",
    "confidence",
}


def load_fixture(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
    except Exception:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("canon fixture root must be an object")
    return data


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = load_fixture(FIXTURE)
    except Exception as exc:
        data = {}
        errors.append(f"failed to load fixture: {exc}")

    components = data.get("components", [])
    techniques = data.get("techniques", [])
    aliases = data.get("alias_rules", [])
    component_by_name = {item.get("component_name"): item for item in components if isinstance(item, dict)}
    technique_by_id = {item.get("technique_id"): item for item in techniques if isinstance(item, dict)}
    alias_pairs = {(item.get("alias"), item.get("canonical")) for item in aliases if isinstance(item, dict)}

    for item in components:
        if not isinstance(item, dict):
            errors.append("component entry must be an object")
            continue
        missing = sorted(REQUIRED_COMPONENT_FIELDS - set(item))
        add(errors, not missing, f"component {item.get('component_name')} missing fields: {missing}")

    for item in techniques:
        if not isinstance(item, dict):
            errors.append("technique entry must be an object")
            continue
        missing = sorted(REQUIRED_TECHNIQUE_FIELDS - set(item))
        add(errors, not missing, f"technique {item.get('technique_id')} missing fields: {missing}")
        add(errors, item.get("primary_sound_type") in ALLOWED_SOUND_TYPES, f"technique {item.get('technique_id')} has invalid primary_sound_type")
        add(errors, item.get("gesture_family") in ALLOWED_GESTURE_FAMILIES, f"technique {item.get('technique_id')} has invalid gesture_family")

    for name, zh in [("bo", "擘"), ("po", "泼"), ("la", "剌"), ("yan", "罨")]:
        comp = component_by_name.get(name)
        add(errors, comp is not None and comp.get("zh_name") == zh, f"required component {name}={zh} missing")
        add(errors, comp is not None and comp.get("standard_internal_name") == name, f"{name} must be standard_internal_name")

    bo = component_by_name.get("bo", {})
    add(errors, "pi" in bo.get("aliases", []) and "劈" in bo.get("aliases", []), "pi/劈 must be bo aliases")
    add(errors, "pi" not in component_by_name, "pi must not be a formal component")
    add(errors, "劈" not in component_by_name, "劈 must not be a formal component")
    add(errors, "拨" not in component_by_name and "撥" not in component_by_name, "拨/撥 must not be internal standard components")

    add(errors, ("拨", "泼") in alias_pairs, "alias 拨 -> 泼 missing")
    add(errors, ("撥", "泼") in alias_pairs, "alias 撥 -> 泼 missing")
    add(errors, ("拨剌", "泼剌") in alias_pairs, "alias 拨剌 -> 泼剌 missing")
    add(errors, ("撥剌", "泼剌") in alias_pairs, "alias 撥剌 -> 泼剌 missing")
    add(errors, ("掩", "罨") in alias_pairs, "alias 掩 -> 罨 missing")

    zhuang = component_by_name.get("zhuang", {})
    add(errors, zhuang.get("component_category") == "micro_returning_slide", "zhuang/撞 must be micro_returning_slide")

    qiaqi = technique_by_id.get("qiaqi", {})
    cuo = technique_by_id.get("cuo", {})
    fanghe = technique_by_id.get("fanghe", {})
    yinghe = technique_by_id.get("yinghe", {})
    fenkai = technique_by_id.get("fenkai", {})
    add(errors, qiaqi.get("gesture_family") == "left_hand_sound", "qiaqi/掐起 must be left_hand_sound")
    add(errors, cuo.get("gesture_family") == "simultaneous_pluck", "cuo/撮 must be simultaneous_pluck")
    add(errors, fanghe.get("gesture_family") == "open_pressed_harmony", "fanghe/放合 must be open_pressed_harmony")
    add(errors, yinghe.get("gesture_family") == "open_pressed_harmony", "yinghe/应合 must be open_pressed_harmony")
    add(errors, fenkai.get("gesture_family") == "compound_both_hands", "fenkai/分开 must be compound_both_hands")
    add(errors, fenkai.get("sound_profile") == "compound_pressed_motion", "fenkai/分开 must use sound_profile=compound_pressed_motion")
    fenkai_components = [rule.get("component_name") for rule in fenkai.get("component_rules", []) if isinstance(rule, dict)]
    add(errors, fenkai_components == ["mo_attack", "shang_motion", "zhu_tiao_return_attack"], "fenkai component chain must be mo_attack, shang_motion, zhu_tiao_return_attack")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "validator": "validate_canon.py",
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "components": len(components),
            "techniques": len(techniques),
            "alias_rules": len(aliases),
        },
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
