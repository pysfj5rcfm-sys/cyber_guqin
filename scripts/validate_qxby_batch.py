#!/usr/bin/env python3
"""Validate QXBY draft ingest without requiring third-party packages."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BATCH_ID = "QXBY_BATCH_001"
DEFAULT_DRAFT = ROOT / "canon" / "drafts" / "qxby_batch_001.yaml"
DEFAULT_REPORT = ROOT / "reports" / "validate_qxby_batch_001_report.json"
DEFAULT_EXPECTED_COUNT = 16

REQUIRED_FIELDS = {
    "item_id",
    "source_id",
    "source_title",
    "batch_id",
    "raw_excerpt",
    "source_status",
    "normalized_term",
    "mapped_component_name",
    "mapped_component_category",
    "mapped_gesture_family",
    "mapped_sound_profile",
    "conflict_with_project_ontology",
    "needs_review",
    "review_status",
    "confidence",
}

QXBY_BATCH_001_EXTRA_REQUIRED_FIELDS = {
    "page_or_section",
    "source_image",
    "normalized_claim",
    "involved_terms",
    "aliases_detected",
    "notes",
}

EXPECTED_QXBY_BATCH_001: dict[str, dict[str, Any]] = {
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
COMPLEX_TECHNIQUE_FAMILIES = {"compound_both_hands", "simultaneous_pluck"}
COMPLEX_TECHNIQUE_CATEGORIES = {"simultaneous_pluck"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-id", default=DEFAULT_BATCH_ID)
    parser.add_argument("--draft", default=relative(DEFAULT_DRAFT))
    parser.add_argument("--expected-count", type=int, default=DEFAULT_EXPECTED_COUNT)
    parser.add_argument("--report", default=relative(DEFAULT_REPORT))
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument("--allow-warnings", action="store_true", help="allow warnings when --strict is set")
    return parser.parse_args()


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value in {"null", "~"}:
        return None
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
    active_list_owner: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line == "items:":
            root["items"] = items
            current = None
            active_list_key = None
            active_list_owner = None
            continue

        if indent == 0 and not line.startswith("- "):
            key, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"cannot parse top-level line: {raw_line}")
            key = key.strip()
            if value.strip():
                root[key] = parse_scalar(value)
                active_list_key = None
                active_list_owner = None
            else:
                root[key] = []
                active_list_key = key
                active_list_owner = root
            current = None
            continue

        if line.startswith("- "):
            payload = line[2:]
            if active_list_owner is not None and active_list_key is not None:
                active_list_owner.setdefault(active_list_key, []).append(parse_scalar(payload))
            elif indent in {0, 2} and "items" in root:
                current = {}
                items.append(current)
                active_list_key = None
                active_list_owner = None
                if payload:
                    key, sep, value = payload.partition(":")
                    if not sep:
                        raise ValueError(f"cannot parse item line: {raw_line}")
                    current[key.strip()] = parse_scalar(value)
            else:
                raise ValueError(f"unsupported list indentation: {raw_line}")
            continue

        if indent == 2 and current is not None:
            key, sep, value = line.partition(":")
            if not sep:
                raise ValueError(f"cannot parse field line: {raw_line}")
            key = key.strip()
            if value.strip():
                current[key] = parse_scalar(value)
                active_list_key = None
                active_list_owner = None
            else:
                current[key] = []
                active_list_key = key
                active_list_owner = current
            continue

        raise ValueError(f"unsupported YAML fallback line: {raw_line}")

    root.setdefault("items", items)
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


def extract_expected_mapping(data: dict[str, Any], batch_id: str) -> dict[str, dict[str, Any]]:
    candidates = data.get("required_items", data.get("expected_items"))
    if isinstance(candidates, dict):
        return {str(term): rules for term, rules in candidates.items() if isinstance(rules, dict)}
    if isinstance(candidates, list):
        mapping: dict[str, dict[str, Any]] = {}
        for entry in candidates:
            if not isinstance(entry, dict):
                continue
            term = entry.get("normalized_term") or entry.get("term") or entry.get("mapped_component_name")
            if term:
                mapping[str(term)] = {str(key): value for key, value in entry.items() if key != "term"}
        return mapping
    if batch_id == DEFAULT_BATCH_ID:
        return EXPECTED_QXBY_BATCH_001
    return {}


def validate_qxby_batch_001_rules(by_term: dict[str, dict[str, Any]], errors: list[str]) -> None:
    bo = by_term.get("bo", {})
    bo_aliases = set(bo.get("aliases_detected", []) if isinstance(bo.get("aliases_detected"), list) else [])
    add(errors, bo.get("mapped_component_name") == "bo", "bo must map to internal component_name=bo")
    add(errors, "pi" in bo_aliases or "鍔?" in bo_aliases, "bo should retain pi/鍔? only as detected aliases when present")
    add(errors, bo.get("mapped_component_name") not in {"pi", "鍔?"}, "pi/鍔? must not become an internal component name")

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


def validate_items(
    data: dict[str, Any],
    batch_id: str,
    expected_count: int,
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    items = data.get("items", [])
    add(errors, isinstance(items, list), "items must be a list")
    if not isinstance(items, list):
        return {}

    item_objects = [item for item in items if isinstance(item, dict)]
    add(errors, len(item_objects) == len(items), "every item must be an object")
    add(errors, len(item_objects) == expected_count, f"draft should contain {expected_count} items, found {len(item_objects)}")

    by_term: dict[str, dict[str, Any]] = {}
    duplicate_terms: list[str] = []
    item_ids: list[str] = []
    duplicate_item_ids: list[str] = []
    for item in item_objects:
        term = str(item.get("normalized_term", ""))
        item_id = str(item.get("item_id", ""))
        if term in by_term:
            duplicate_terms.append(term)
        if item_id in item_ids:
            duplicate_item_ids.append(item_id)
        by_term[term] = item
        item_ids.append(item_id)

    expected_mapping = extract_expected_mapping(data, batch_id)
    if expected_mapping:
        expected_terms = set(expected_mapping)
        actual_terms = set(by_term)
        missing_terms = sorted(expected_terms - actual_terms)
        extra_terms = sorted(actual_terms - expected_terms)
        add(errors, not missing_terms, f"missing {batch_id} required terms: {missing_terms}")
        add(errors, not extra_terms, f"unexpected terms in {batch_id} draft: {extra_terms}")
    add(errors, not duplicate_terms, f"duplicate normalized_term values: {sorted(duplicate_terms)}")
    add(errors, not duplicate_item_ids, f"duplicate item_id values: {sorted(duplicate_item_ids)}")

    required_fields = set(REQUIRED_FIELDS)
    if batch_id == DEFAULT_BATCH_ID:
        required_fields |= QXBY_BATCH_001_EXTRA_REQUIRED_FIELDS

    for term, item in by_term.items():
        missing_fields = sorted(required_fields - set(item))
        add(errors, not missing_fields, f"{term}: missing required fields {missing_fields}")
        add(errors, item.get("source_id") == batch_id, f"{term}: source_id must be {batch_id}")
        add(errors, item.get("batch_id") == batch_id, f"{term}: batch_id must be {batch_id}")
        add(errors, item.get("confidence") in ALLOWED_CONFIDENCE, f"{term}: confidence must be one of {sorted(ALLOWED_CONFIDENCE)}")
        add(errors, "conflict_with_project_ontology" in item, f"{term}: conflict_with_project_ontology field must exist")
        if "conflict_with_project_ontology" in item:
            add(
                errors,
                item.get("conflict_with_project_ontology") is False or item.get("conflict_with_project_ontology") is True,
                f"{term}: conflict_with_project_ontology must be boolean",
            )

        source_status = str(item.get("source_status", ""))
        review_status = str(item.get("review_status", ""))
        if "ocr" in source_status.lower():
            add(errors, review_status != "verified", f"{term}: OCR candidate item must not be verified")
        if source_status == "manual_image_transcription":
            add(errors, review_status != "verified", f"{term}: manual_image_transcription item must not be verified")
        if batch_id == DEFAULT_BATCH_ID:
            add(errors, source_status == "manual_image_transcription", f"{term}: source_status must be manual_image_transcription")
            add(errors, review_status == "draft", f"{term}: review_status must stay draft")
            add(errors, item.get("needs_review") is True, f"{term}: needs_review must be true")

        if item.get("mapped_component_category") == "pre_slide":
            add(errors, item.get("mapped_sound_profile") != "post_motion", f"{term}: pre_slide must not use mapped_sound_profile=post_motion")
        if item.get("mapped_gesture_family") == "component_only":
            add(errors, item.get("mapped_component_category") == "pre_slide", f"{term}: component_only is only allowed as a draft-local pre_slide marker")

        is_complex = (
            item.get("mapped_gesture_family") in COMPLEX_TECHNIQUE_FAMILIES
            or item.get("mapped_component_category") in COMPLEX_TECHNIQUE_CATEGORIES
        )
        if is_complex:
            add(errors, "primary_sound_type" not in item or item.get("primary_sound_type") in {"", None}, f"{term}: complex technique must not use primary_sound_type as a fourth sound type")

    for term, expected in expected_mapping.items():
        item = by_term.get(term)
        if item is not None:
            check_expected_mapping(errors, item, term, expected)

    if batch_id == DEFAULT_BATCH_ID:
        validate_qxby_batch_001_rules(by_term, errors)

    conflicts = sorted(term for term, item in by_term.items() if item.get("conflict_with_project_ontology") is True)
    uncertain = sorted(
        term
        for term, item in by_term.items()
        if item.get("confidence") in {"medium", "low"} or "寰?" in str(item.get("page_or_section", "")) or "鐤?" in str(item.get("notes", ""))
    )

    summary = {
        "batch_id": data.get("batch_id", batch_id),
        "source_title": data.get("source_title"),
        "source_status": data.get("source_status"),
        "item_count": len(item_objects),
        "expected_count": expected_count,
        "required_item_count": len(expected_mapping),
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
    return summary


def write_report(
    errors: list[str],
    warnings: list[str],
    summary: dict[str, Any],
    draft: Path,
    report_path: Path,
    args: argparse.Namespace,
) -> int:
    effective_errors = list(errors)
    if args.strict and warnings and not args.allow_warnings:
        effective_errors.extend(f"strict warning: {warning}" for warning in warnings)
    status = "fail" if effective_errors else ("warning" if warnings else "pass")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "validator": "validate_qxby_batch.py",
        "input": relative(draft),
        "batch_id": args.batch_id,
        "expected_count": args.expected_count,
        "strict": args.strict,
        "allow_warnings": args.allow_warnings,
        "status": status,
        "passed": not effective_errors,
        "errors": effective_errors,
        "warnings": warnings,
        "summary": summary,
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not effective_errors else 1


def main() -> int:
    args = parse_args()
    draft = resolve_path(args.draft)
    report = resolve_path(args.report)
    errors: list[str] = []
    warnings: list[str] = []

    add(errors, draft.exists(), f"missing draft file: {relative(draft)}")
    data: dict[str, Any] = {}
    if draft.exists():
        try:
            data = load_draft(draft, warnings)
        except Exception as exc:
            errors.append(str(exc))

    summary = validate_items(data, args.batch_id, args.expected_count, errors, warnings) if data else {}
    return write_report(errors, warnings, summary, draft, report, args)


if __name__ == "__main__":
    raise SystemExit(main())
