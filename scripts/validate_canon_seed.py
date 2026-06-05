#!/usr/bin/env python3
"""Validate Step 2A canon seed files without requiring third-party packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canon"
REPORT = ROOT / "reports" / "validate_canon_seed_report.json"

REQUIRED_FILES = {
    "sources.yaml",
    "terms.yaml",
    "component_lexicon.yaml",
    "gesture_families.yaml",
    "alias_rules.yaml",
    "technique_rules.yaml",
    "validation_rules.yaml",
}

ALLOWED_SOUND_TYPES = {"散音", "按音", "泛音", "none"}
ALLOWED_COMPONENT_CATEGORIES = {
    "pluck",
    "pre_slide",
    "single_slide",
    "returning_slide",
    "micro_returning_slide",
    "vibrato",
    "left_sound",
    "right_sequence",
    "simultaneous_pluck",
    "open_pressed_harmony",
    "compound_both_hands",
}
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
REQUIRED_TERM_FIELDS = {"term_id", "name_zh", "definition", "category", "source_refs", "review_status"}
REQUIRED_ALIAS_FIELDS = {"alias", "canonical", "alias_type", "scope", "notes", "source_refs", "review_status"}
REQUIRED_FAMILY_FIELDS = {
    "gesture_family",
    "zh_name",
    "description",
    "examples",
    "requires_components",
    "default_requires_context_sample",
    "review_status",
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


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def warn(warnings: list[str], condition: bool, message: str) -> None:
    if not condition:
        warnings.append(message)


def load_seed(path: Path, warnings: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore

            data = yaml.safe_load(text)
            warnings.append(f"{path.name}: parsed with optional PyYAML fallback")
        except Exception as exc:
            raise ValueError(f"{path.name}: cannot parse as JSON-compatible YAML and PyYAML was unavailable or failed: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"{path.name}: root must be an object")
    return data


def require_fields(errors: list[str], kind: str, item: Any, required: set[str], name: str) -> None:
    if not isinstance(item, dict):
        errors.append(f"{kind} {name} must be an object")
        return
    missing = sorted(required - set(item))
    add(errors, not missing, f"{kind} {name} missing fields: {missing}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    loaded: dict[str, dict[str, Any]] = {}

    missing = sorted(name for name in REQUIRED_FILES if not (CANON / name).exists())
    add(errors, not missing, f"missing canon seed files: {missing}")

    for name in sorted(REQUIRED_FILES):
        path = CANON / name
        if not path.exists():
            continue
        try:
            loaded[name] = load_seed(path, warnings)
        except Exception as exc:
            errors.append(str(exc))

    sources = loaded.get("sources.yaml", {}).get("sources", [])
    terms = loaded.get("terms.yaml", {}).get("terms", [])
    components = loaded.get("component_lexicon.yaml", {}).get("components", [])
    families = loaded.get("gesture_families.yaml", {}).get("gesture_families", [])
    aliases = loaded.get("alias_rules.yaml", {}).get("alias_rules", [])
    techniques = loaded.get("technique_rules.yaml", {}).get("techniques", [])
    rules = loaded.get("validation_rules.yaml", {}).get("validation_rules", [])

    for collection_name, collection in [
        ("sources", sources),
        ("terms", terms),
        ("components", components),
        ("gesture_families", families),
        ("alias_rules", aliases),
        ("techniques", techniques),
        ("validation_rules", rules),
    ]:
        add(errors, isinstance(collection, list), f"{collection_name} must be a list")

    if not all(isinstance(collection, list) for collection in [sources, terms, components, families, aliases, techniques, rules]):
        return write_report(errors, warnings, {})

    source_ids = {item.get("source_id") for item in sources if isinstance(item, dict)}
    add(errors, "PROJECT_ONTOLOGY_V1_1" in source_ids, "source PROJECT_ONTOLOGY_V1_1 missing")

    for item in terms:
        require_fields(errors, "term", item, REQUIRED_TERM_FIELDS, str(item.get("term_id") if isinstance(item, dict) else "<invalid>"))

    for item in components:
        name = str(item.get("component_name") if isinstance(item, dict) else "<invalid>")
        require_fields(errors, "component", item, REQUIRED_COMPONENT_FIELDS, name)
        if isinstance(item, dict):
            add(errors, item.get("component_category") in ALLOWED_COMPONENT_CATEGORIES, f"component {name} invalid component_category")

    for item in families:
        name = str(item.get("gesture_family") if isinstance(item, dict) else "<invalid>")
        require_fields(errors, "gesture_family", item, REQUIRED_FAMILY_FIELDS, name)
        if isinstance(item, dict):
            add(errors, item.get("gesture_family") in ALLOWED_GESTURE_FAMILIES, f"gesture_family {name} invalid")
            add(errors, item.get("gesture_family") != "pressed_compound_motion", "pressed_compound_motion must not be a gesture_family")

    for item in aliases:
        name = str(item.get("alias") if isinstance(item, dict) else "<invalid>")
        require_fields(errors, "alias_rule", item, REQUIRED_ALIAS_FIELDS, name)

    for item in techniques:
        name = str(item.get("technique_id") if isinstance(item, dict) else "<invalid>")
        require_fields(errors, "technique", item, REQUIRED_TECHNIQUE_FIELDS, name)
        if isinstance(item, dict):
            add(errors, item.get("primary_sound_type") in ALLOWED_SOUND_TYPES, f"technique {name} invalid primary_sound_type")
            add(errors, item.get("gesture_family") in ALLOWED_GESTURE_FAMILIES, f"technique {name} invalid gesture_family")

    component_by_name = {item.get("component_name"): item for item in components if isinstance(item, dict)}
    technique_by_id = {item.get("technique_id"): item for item in techniques if isinstance(item, dict)}
    alias_pairs = {(item.get("alias"), item.get("canonical")) for item in aliases if isinstance(item, dict)}
    family_names = {item.get("gesture_family") for item in families if isinstance(item, dict)}
    rule_text = "\n".join(json.dumps(item, ensure_ascii=False) for item in rules if isinstance(item, dict))

    for name, zh in [("bo", "擘"), ("po", "泼"), ("la", "剌"), ("yan", "罨")]:
        comp = component_by_name.get(name, {})
        add(errors, bool(comp) and comp.get("zh_name") == zh, f"required component {name}={zh} missing")
        add(errors, bool(comp) and comp.get("standard_internal_name") == name, f"{name} must be its standard_internal_name")

    bo = component_by_name.get("bo", {})
    add(errors, "pi" in bo.get("aliases", []) and "劈" in bo.get("aliases", []), "pi/劈 must be bo aliases")
    add(errors, "pi" not in component_by_name and "劈" not in component_by_name, "pi/劈 must not be formal component names")
    add(errors, "拨" not in component_by_name and "撥" not in component_by_name, "拨/撥 must not be internal standard components")

    for pair in [
        ("劈", "擘"),
        ("pi", "bo"),
        ("拨", "泼"),
        ("撥", "泼"),
        ("拨剌", "泼剌"),
        ("撥剌", "泼剌"),
        ("掩", "罨"),
        ("虚掩", "虚罨"),
        ("搯起", "掐起"),
    ]:
        add(errors, pair in alias_pairs, f"alias {pair[0]} -> {pair[1]} missing")

    for name in ["zhuang", "fan_zhuang"]:
        comp = component_by_name.get(name, {})
        add(errors, comp.get("component_category") == "micro_returning_slide", f"{name} must be micro_returning_slide")
        add(errors, "percussive" not in comp, f"{name} must not use percussive field")

    for name in ["jinfu", "tuifu"]:
        comp = component_by_name.get(name, {})
        add(errors, comp.get("component_category") == "returning_slide", f"{name} must be returning_slide")
        description = str(comp.get("description", ""))
        add(errors, "原子" in description or "不拆" in description, f"{name} must be documented as atomic")

    for name in ["qiaqi", "yan", "daiqi"]:
        comp = component_by_name.get(name, {})
        add(errors, comp.get("component_category") == "left_sound", f"{name} component must be left_sound")

    add(errors, component_by_name.get("cuo", {}).get("component_category") == "simultaneous_pluck", "cuo component must be simultaneous_pluck")
    add(errors, component_by_name.get("fenkai", {}).get("component_category") != "open_pressed_harmony", "fenkai component must not be open_pressed_harmony")
    add(errors, "pressed_compound_motion" not in family_names, "pressed_compound_motion must not be created as gesture_family")

    expected_families = ALLOWED_GESTURE_FAMILIES
    add(errors, expected_families <= family_names, f"missing gesture family seed entries: {sorted(expected_families - family_names)}")

    for technique_id, family in [
        ("shang", "post_motion"),
        ("zhuang", "post_motion"),
        ("qiaqi", "left_hand_sound"),
        ("cuo", "simultaneous_pluck"),
        ("po_la", "right_hand_sequence"),
        ("gun_fu", "right_hand_sequence"),
        ("fanghe", "open_pressed_harmony"),
        ("yinghe", "open_pressed_harmony"),
        ("fenkai", "compound_both_hands"),
    ]:
        tech = technique_by_id.get(technique_id, {})
        add(errors, tech.get("gesture_family") == family, f"{technique_id} technique must be gesture_family={family}")

    fenkai = technique_by_id.get("fenkai", {})
    add(errors, fenkai.get("sound_profile") == "compound_pressed_motion", "fenkai must use sound_profile=compound_pressed_motion")
    fenkai_components = [rule.get("component_name") for rule in fenkai.get("component_rules", []) if isinstance(rule, dict)]
    add(errors, fenkai_components == ["mo_attack", "shang_motion", "zhu_tiao_return_attack"], "fenkai component chain must be mo_attack, shang_motion, zhu_tiao_return_attack")
    add(errors, "xia" not in fenkai_components and "下" not in json.dumps(fenkai.get("component_rules", []), ensure_ascii=False), "fenkai must not add extra 下")
    add(errors, "score-unmarked chuo" in rule_text, "score-unmarked chuo validation rule missing")

    warn(
        warnings,
        all(path.read_text(encoding="utf-8").lstrip().startswith("{") for path in CANON.glob("*.yaml")),
        "seed files are not fully JSON-compatible YAML; standard-library fallback may be limited",
    )

    summary = {
        "sources": len(sources),
        "terms": len(terms),
        "components": len(components),
        "gesture_families": len(families),
        "alias_rules": len(aliases),
        "techniques": len(techniques),
        "validation_rules": len(rules),
    }
    return write_report(errors, warnings, summary)


def write_report(errors: list[str], warnings: list[str], summary: dict[str, Any]) -> int:
    status = "fail" if errors else ("warning" if warnings else "pass")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "validator": "validate_canon_seed.py",
        "status": status,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "inputs": sorted(str(path.relative_to(ROOT)) for path in CANON.glob("*.yaml")),
        "summary": summary,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
