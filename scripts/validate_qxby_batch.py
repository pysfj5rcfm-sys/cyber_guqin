#!/usr/bin/env python3
"""Validate QXBY_BATCH_001 draft ingest without requiring third-party packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "canon" / "drafts" / "qxby_batch_001.yaml"
REPORT = ROOT / "reports" / "validate_qxby_batch_001_report.json"

REQUIRED_FIELDS = {
    "item_id",
    "source_id",
    "source_title",
    "batch_id",
    "page_or_section",
    "source_image",
    "raw_excerpt",
    "source_status",
    "normalized_term",
    "normalized_claim",
    "involved_terms",
    "mapped_component_name",
    "mapped_component_category",
    "mapped_gesture_family",
    "mapped_sound_profile",
    "aliases_detected",
    "conflict_with_project_ontology",
    "needs_review",
    "review_status",
    "confidence",
    "notes",
}

EXPECTED: dict[str, dict[str, Any]] = {
    "bo": {
        "mapped_component_name": "bo",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "tuo": {
        "mapped_component_name": "tuo",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "mo": {
        "mapped_component_name": "mo",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "tiao": {
        "mapped_component_name": "tiao",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "gou": {
        "mapped_component_name": "gou",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "ti": {
        "mapped_component_name": "ti",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "da": {
        "mapped_component_name": "da",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "zhai": {
        "mapped_component_name": "zhai",
        "mapped_component_category": "pluck",
        "mapped_gesture_family": "single_pluck",
        "mapped_sound_profile": "single",
    },
    "chuo": {
        "mapped_component_name": "chuo",
        "mapped_component_category": "pre_slide",
        "mapped_gesture_family": "component_only",
        "mapped_sound_profile": "none",
        "claim_contains": "notation_pre_action=chuo",
    },
    "zhu": {
        "mapped_component_name": "zhu",
        "mapped_component_category": "pre_slide",
        "mapped_gesture_family": "component_only",
        "mapped_sound_profile": "none",
        "claim_contains": "notation_pre_action=zhu",
    },
    "zhuang": {
        "mapped_component_name": "zhuang",
        "mapped_component_category": "micro_returning_slide",
        "mapped_gesture_family": "post_motion",
    },
    "fan_zhuang": {
        "mapped_component_name": "fan_zhuang",
        "mapped_component_category": "micro_returning_slide",
        "mapped_gesture_family": "post_motion",
    },
    "shang": {
        "mapped_component_name": "shang",
        "mapped_component_category": "single_slide",
        "mapped_gesture_family": "post_motion",
    },
    "xia": {
        "mapped_component_name": "xia",
        "mapped_component_category": "single_slide",
        "mapped_gesture_family": "post_motion",
    },
    "qiaqi": {
        "mapped_component_name": "qiaqi",
        "mapped_component_category": "left_sound",
        "mapped_gesture_family": "left_hand_sound",
    },
    "cuo": {
        "mapped_component_name": "cuo",
        "mapped_component_category": "simultaneous_pluck",
        "mapped_gesture_family": "simultaneous_pluck",
    },
}

GLOBAL_GUARDRAILS: dict[str, dict[str, Any]] = {
    "po": {"mapped_component_name": "po"},
    "la": {"mapped_component_name": "la"},
    "po_la": {"mapped_component_name": "po_la"},
    "yan": {"mapped_component_name": "yan", "mapped_gesture_family": "left_hand_sound"},
    "daiqi": {"mapped_component_name": "daiqi", "mapped_gesture_family": "left_hand_sound"},
    "jinfu": {"mapped_component_category": "returning_slide"},
    "tuifu": {"mapped_component_category": "returning_slide"},
    "fanghe": {"mapped_gesture_family": "open_pressed_harmony"},
    "yinghe": {"mapped_gesture_family": "open_pressed_harmony"},
    "fenkai": {
        "mapped_gesture_family": "compound_both_hands",
        "mapped_sound_profile": "compound_pressed_motion",
    },
    "qia_cuo_sansheng": {"mapped_gesture_family": "compound_both_hands"},
}

ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "[]":
        return []
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    return value


def load_fallback_yaml(text: str) -> dict[str, Any]:
    """Small fallback parser for this draft's simple mapping/list shape."""
    root: dict[str, Any] = {}
    items: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    active_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line == "items:":
            root["items"] = items
            current = None
            active_list_key = None
            continue

        if indent == 0:
            key, _, value = line.partition(":")
            if not _:
                raise ValueError(f"cannot parse top-level line: {raw_line}")
            root[key] = parse_scalar(value)
            active_list_key = None
            continue

        if line.startswith("- "):
            payload = line[2:]
            if indent == 0:
                raise ValueError(f"unexpected root list line: {raw_line}")
            if indent == 2:
                if current is None or active_list_key is None:
                    current = {}
                    items.append(current)
                    active_list_key = None
                    if payload:
                        key, _, value = payload.partition(":")
                        if not _:
                            raise ValueError(f"cannot parse item line: {raw_line}")
                        current[key] = parse_scalar(value)
                else:
                    current.setdefault(active_list_key, []).append(parse_scalar(payload))
            elif indent == 4 and current is not None and active_list_key is not None:
                current.setdefault(active_list_key, []).append(parse_scalar(payload))
            else:
                raise ValueError(f"unsupported list indentation: {raw_line}")
            continue

        if indent == 2 and current is not None:
            key, _, value = line.partition(":")
            if not _:
                raise ValueError(f"cannot parse field line: {raw_line}")
            if value.strip():
                current[key] = parse_scalar(value)
                active_list_key = None
            else:
                current[key] = []
                active_list_key = key
            continue

        raise ValueError(f"unsupported YAML fallback line: {raw_line}")

    if "items" not in root:
        root["items"] = items
    return root


def load_draft(path: Path, warnings: list[str]) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore

            parsed = yaml.safe_load(text)
        except Exception:
            parsed = load_fallback_yaml(text)
    if not isinstance(parsed, dict):
        raise ValueError("draft root must be an object")
    return parsed


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def warn(warnings: list[str], condition: bool, message: str) -> None:
    if not condition:
        warnings.append(message)


def check_expected_mapping(errors: list[str], item: dict[str, Any], term: str, expected: dict[str, Any]) -> None:
    for key, value in expected.items():
        if key == "claim_contains":
            add(errors, value in str(item.get("normalized_claim", "")), f"{term}: normalized_claim must contain {value}")
        else:
            add(errors, item.get(key) == value, f"{term}: expected {key}={value}, got {item.get(key)!r}")


def check_no_mapping_value(errors: list[str], item: dict[str, Any], term: str, forbidden: set[str]) -> None:
    for key, value in item.items():
        if key in {"raw_excerpt", "normalized_claim", "notes"}:
            continue
        if isinstance(value, str) and value in forbidden:
            errors.append(f"{term}: field {key} must not be {value}")
        if isinstance(value, list) and any(entry in forbidden for entry in value):
            errors.append(f"{term}: field {key} must not include forbidden values {sorted(forbidden)}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    add(errors, DRAFT.exists(), f"missing draft file: {DRAFT.relative_to(ROOT)}")
    data: dict[str, Any] = {}
    if DRAFT.exists():
        try:
            data = load_draft(DRAFT, warnings)
        except Exception as exc:
            errors.append(str(exc))

    items = data.get("items", [])
    add(errors, isinstance(items, list), "items must be a list")
    if not isinstance(items, list):
        return write_report(errors, warnings, {})

    item_objects = [item for item in items if isinstance(item, dict)]
    add(errors, len(item_objects) == len(items), "every item must be an object")

    by_term: dict[str, dict[str, Any]] = {}
    duplicate_terms: list[str] = []
    for item in item_objects:
        term = str(item.get("normalized_term", ""))
        if term in by_term:
            duplicate_terms.append(term)
        by_term[term] = item

    expected_terms = set(EXPECTED)
    actual_terms = set(by_term)
    missing_terms = sorted(expected_terms - actual_terms)
    extra_terms = sorted(actual_terms - expected_terms)
    add(errors, not missing_terms, f"missing QXBY_BATCH_001 required terms: {missing_terms}")
    add(errors, not extra_terms, f"unexpected terms in QXBY_BATCH_001 draft: {extra_terms}")
    add(errors, not duplicate_terms, f"duplicate normalized_term values: {sorted(duplicate_terms)}")

    for term, item in by_term.items():
        missing_fields = sorted(REQUIRED_FIELDS - set(item))
        add(errors, not missing_fields, f"{term}: missing required fields {missing_fields}")
        add(errors, item.get("source_id") == "QXBY_BATCH_001", f"{term}: source_id must be QXBY_BATCH_001")
        add(errors, item.get("batch_id") == "QXBY_BATCH_001", f"{term}: batch_id must be QXBY_BATCH_001")
        add(errors, item.get("source_status") == "manual_image_transcription", f"{term}: source_status must be manual_image_transcription")
        add(errors, item.get("review_status") == "draft", f"{term}: review_status must stay draft")
        add(errors, item.get("needs_review") is True, f"{term}: needs_review must be true")
        add(errors, item.get("confidence") in ALLOWED_CONFIDENCE, f"{term}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        add(errors, item.get("review_status") != "verified", f"{term}: manual transcription item must not be verified")
        add(errors, item.get("conflict_with_project_ontology") is False or item.get("conflict_with_project_ontology") is True, f"{term}: conflict_with_project_ontology must be boolean")
        if item.get("mapped_component_category") == "pre_slide":
            add(errors, item.get("mapped_sound_profile") != "post_motion", f"{term}: pre_slide must not use mapped_sound_profile=post_motion")
        if item.get("mapped_gesture_family") == "component_only":
            add(errors, item.get("mapped_component_category") == "pre_slide", f"{term}: component_only is only allowed as a draft-local pre_slide marker")

    for term, expected in EXPECTED.items():
        item = by_term.get(term)
        if item is None:
            continue
        check_expected_mapping(errors, item, term, expected)

    bo = by_term.get("bo", {})
    bo_aliases = set(bo.get("aliases_detected", []) if isinstance(bo.get("aliases_detected"), list) else [])
    add(errors, bo.get("mapped_component_name") == "bo", "bo must map to internal component_name=bo")
    add(errors, "pi" in bo_aliases or "劈" in bo_aliases, "bo should retain pi/劈 only as detected aliases when present")
    add(errors, bo.get("mapped_component_name") not in {"pi", "劈"}, "pi/劈 must not become an internal component name")

    for term in ["chuo", "zhu"]:
        item = by_term.get(term)
        if item is not None:
            add(errors, item.get("mapped_sound_profile") == "none", f"{term}: mapped_sound_profile must be none")
            add(errors, item.get("mapped_gesture_family") == "component_only", f"{term}: component_only is allowed only as a draft-local marker, not a canonical gesture_family")

    for term in ["zhuang", "fan_zhuang"]:
        item = by_term.get(term)
        if item is not None:
            check_no_mapping_value(errors, item, term, {"percussive"})

    qiaqi = by_term.get("qiaqi")
    if qiaqi is not None:
        check_no_mapping_value(errors, qiaqi, "qiaqi", {"right_hand_action", "simultaneous_pluck"})

    cuo = by_term.get("cuo")
    if cuo is not None:
        add(errors, "sound_type" not in cuo, "cuo must not create a sound_type field")
        add(errors, cuo.get("mapped_sound_profile") != "sound_type", "cuo must not be encoded as a fourth sound_type")

    for term, expected in GLOBAL_GUARDRAILS.items():
        item = by_term.get(term)
        if item is None:
            continue
        check_expected_mapping(errors, item, term, expected)
        if term in {"jinfu", "tuifu"}:
            text = json.dumps(item, ensure_ascii=False)
            add(errors, "+" not in text and "split" not in text.lower(), f"{term}: returning slide must remain atomic")
        if term == "fenkai":
            text = json.dumps(item, ensure_ascii=False)
            add(errors, "open_pressed_harmony" not in text, "fenkai must not be open_pressed_harmony")

    conflicts = sorted(term for term, item in by_term.items() if item.get("conflict_with_project_ontology") is True)
    uncertain = sorted(
        term
        for term, item in by_term.items()
        if item.get("confidence") in {"medium", "low"} or "待" in str(item.get("page_or_section", "")) or "疑" in str(item.get("notes", ""))
    )

    summary = {
        "batch_id": data.get("batch_id", "QXBY_BATCH_001"),
        "source_title": data.get("source_title"),
        "source_status": data.get("source_status"),
        "item_count": len(item_objects),
        "required_item_count": len(EXPECTED),
        "terms": sorted(by_term),
        "confidence": {
            level: sorted(term for term, item in by_term.items() if item.get("confidence") == level)
            for level in ["high", "medium", "low"]
        },
        "conflicts_with_project_ontology": conflicts,
        "ocr_or_transcription_uncertainty_terms": uncertain,
        "global_guardrails_checked_when_present": sorted(term for term in GLOBAL_GUARDRAILS if term in by_term),
        "global_guardrails_not_required_when_absent": sorted(term for term in GLOBAL_GUARDRAILS if term not in by_term),
    }

    warn(warnings, not conflicts, f"items marked conflict_with_project_ontology=true: {conflicts}")
    return write_report(errors, warnings, summary)


def write_report(errors: list[str], warnings: list[str], summary: dict[str, Any]) -> int:
    status = "fail" if errors else ("warning" if warnings else "pass")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "validator": "validate_qxby_batch.py",
        "input": str(DRAFT.relative_to(ROOT)),
        "status": status,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
