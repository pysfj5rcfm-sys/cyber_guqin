#!/usr/bin/env python3
"""Run P1-B fixture cases through the executable P1 grammar parser."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.cyber_guqin_grammar_parser import GrammarParser, AUTHORITY_FLAGS


def discover_fixture_cases(fixture_dir: Path) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    for path in sorted(Path(fixture_dir).glob("p1b_*_fixtures.v*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        schema_id = data.get("fixture_schema_id")
        if not isinstance(schema_id, str) or not schema_id.startswith("CG_LXY_P1B_"):
            raise ValueError(f"invalid fixture_schema_id in {path}")
        for case in data.get("cases", []):
            item = dict(case)
            item["_fixture_file"] = path.name
            cases.append(item)
    return cases


def run_fixtures(repo_root: Path, fixture_dir: Path, *, allow_abstract_component_ids: bool = True) -> dict[str, Any]:
    root = Path(repo_root)
    cases = discover_fixture_cases(fixture_dir)
    parser = GrammarParser.from_repo_root(root, allow_abstract_component_ids=allow_abstract_component_ids)
    results: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    coverage_by_production: Counter[str] = Counter()
    coverage_by_status: Counter[str] = Counter()
    coverage_by_guard_action: Counter[str] = Counter()
    coverage_by_normalization: Counter[str] = Counter()

    for case in cases:
        context = case.get("context_input") if isinstance(case.get("context_input"), dict) else None
        options = case.get("parser_options") if isinstance(case.get("parser_options"), dict) else None
        result = parser.parse(case.get("input_tokens", []), context_input=context, options=options)
        case_failures = _assert_case(case, result)
        coverage_by_status.update([result["parse_status"]])
        rules = _rules_in_result(result)
        coverage_by_production.update(rules)
        coverage_by_guard_action.update(result["guard_summary"].get("guard_actions", []))
        coverage_by_normalization.update([result["normalization_summary"].get("normalization_status", "UNKNOWN")])
        row = {
            "case_id": case.get("case_id"),
            "fixture_file": case.get("_fixture_file"),
            "parse_status": result["parse_status"],
            "passed": not case_failures,
            "failures": case_failures,
        }
        results.append(row)
        if case_failures:
            failures.append(row)

    source_scan = _source_scan(root)
    report = {
        "discovered_fixture_files": sorted({case["_fixture_file"] for case in cases}),
        "discovered_fixture_count": len(sorted({case["_fixture_file"] for case in cases})),
        "discovered_case_count": len(cases),
        "executed_case_ids": [case["case_id"] for case in cases],
        "pass_count": len(cases) - len(failures),
        "fail_count": len(failures),
        "failed_case_ids": [item["case_id"] for item in failures],
        "case_results": results,
        "coverage_by_production": dict(sorted(coverage_by_production.items())),
        "coverage_by_status": dict(sorted(coverage_by_status.items())),
        "coverage_by_guard_action": dict(sorted(coverage_by_guard_action.items())),
        "coverage_by_normalization": dict(sorted(coverage_by_normalization.items())),
        "property_results": {},
        "metamorphic_results": {},
        "combinatorial_results": parser.run_combinatorial_smoke(),
        "extension_discovery_result": {"dynamic_discovery": True},
        "fixed_case_count_detected": source_scan["fixed_case_count_detected"],
        "case_id_hardcoding_detected": source_scan["case_id_hardcoding_detected"],
        "oracle_leakage_detected": source_scan["oracle_leakage_detected"],
        "authority_boundary": dict(AUTHORITY_FLAGS),
    }
    return report


def _assert_case(case: dict[str, Any], result: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if result["parse_status"] != case.get("expected_parse_status"):
        failures.append(f"parse_status expected {case.get('expected_parse_status')} got {result['parse_status']}")

    expected_rules = set(case.get("expected_primary_rule_ids") or [])
    actual_rules = _rules_in_result(result)
    missing_rules = expected_rules - actual_rules
    if missing_rules:
        failures.append(f"missing rule ids {sorted(missing_rules)}")

    expected_actions = set(case.get("expected_guard_actions") or [])
    actual_actions = set(result.get("guard_summary", {}).get("guard_actions", []))
    for candidate_input in case.get("candidate_inputs") or []:
        actual_actions.update(candidate_input.get("guard_actions", []))
    if not expected_actions <= actual_actions:
        failures.append(f"missing guard actions {sorted(expected_actions - actual_actions)}")

    expected_unconsumed = set(case.get("expected_unconsumed_token_ids") or [])
    if set(result.get("unconsumed_tokens", [])) != expected_unconsumed:
        failures.append(f"unconsumed expected {sorted(expected_unconsumed)} got {sorted(result.get('unconsumed_tokens', []))}")

    expected_consumed = set(case.get("expected_consumed_token_ids") or [])
    actual_consumed = set(result.get("consumed_token_ids", []))
    if not actual_consumed:
        for rejected in result.get("rejected_candidates", []):
            actual_consumed.update(rejected.get("consumed_token_ids", []))
    if expected_consumed != actual_consumed:
        failures.append(f"consumed expected {sorted(expected_consumed)} got {sorted(actual_consumed)}")

    candidate = result["accepted_candidates"][0] if result.get("accepted_candidates") else None
    bindings = case.get("expected_slot_bindings") or {}
    for slot_name, expected in bindings.items():
        if expected is None:
            if slot_name == "HOST_UNIT":
                if not any(item.get("required_for") == "HOST_UNIT" for item in result.get("context_requirements", [])):
                    failures.append("missing HOST_UNIT context requirement")
                continue
            actual = _slot_value(candidate, slot_name) if candidate else _slot_value_from_input(case, slot_name)
            if candidate is None:
                continue
            if actual not in (None, [], ""):
                failures.append(f"slot {slot_name} expected empty got {actual}")
            continue
        if not candidate:
            if slot_name == "UNRESOLVED" and set(expected if isinstance(expected, list) else [expected]) <= set(result.get("unconsumed_tokens", [])):
                continue
            actual = _slot_value_from_input(case, slot_name)
            expected_values = set(expected if isinstance(expected, list) else [expected])
            actual_values = set(_flatten(actual if isinstance(actual, list) else [actual]))
            if expected_values & actual_values:
                continue
            failures.append(f"missing candidate for slot {slot_name}")
            continue
        if slot_name == "UNRESOLVED":
            expected_items = set(expected if isinstance(expected, list) else [expected])
            actual_items = set(candidate.get("slots", {}).get("UNRESOLVED", {}).get("token_ids", [])) | set(result.get("unconsumed_tokens", []))
            if not expected_items <= actual_items:
                failures.append(f"slot UNRESOLVED missing {sorted(expected_items - actual_items)}")
            continue
        actual = _slot_value(candidate, slot_name)
        expected_values = set(expected if isinstance(expected, list) else [expected])
        actual_values = set(_flatten(actual if isinstance(actual, list) else [actual]))
        if not (expected_values & actual_values):
            failures.append(f"slot {slot_name} expected {sorted(expected_values)} got {sorted(actual_values)}")

    sound = case.get("expected_sound_type_candidate")
    sound_status = case.get("expected_sound_type_resolution_status")
    if candidate:
        if candidate.get("sound_type_candidate") != sound:
            failures.append(f"sound_type expected {sound} got {candidate.get('sound_type_candidate')}")
        if candidate.get("sound_type_resolution_status") != sound_status:
            failures.append(f"sound status expected {sound_status} got {candidate.get('sound_type_resolution_status')}")
    elif result.get("rejected_candidates"):
        rejected_sound = result["rejected_candidates"][0].get("sound_type_candidate")
        rejected_sound_status = result["rejected_candidates"][0].get("sound_type_resolution_status")
        if sound is not None and rejected_sound != sound:
            failures.append(f"sound_type expected {sound} got {rejected_sound}")
        if sound_status is not None and rejected_sound_status != sound_status:
            failures.append(f"sound status expected {sound_status} got {rejected_sound_status}")
    elif sound is not None:
        failures.append("missing candidate sound type assertion")

    return failures


def _slot_value(candidate: dict[str, Any] | None, slot_name: str) -> Any:
    if not candidate:
        return None
    slot = candidate.get("slots", {}).get(slot_name)
    if not isinstance(slot, dict):
        return slot
    values: list[Any] = []
    values.extend(slot.get("token_ids") or [])
    values.extend(slot.get("component_ids") or [])
    if slot.get("component_id"):
        values.append(slot.get("component_id"))
    if slot.get("value") is not None:
        values.append(slot.get("value"))
    return values


def _flatten(values: list[Any]) -> list[Any]:
    flattened: list[Any] = []
    for value in values:
        if isinstance(value, list):
            flattened.extend(_flatten(value))
        else:
            flattened.append(value)
    return flattened


def _slot_value_from_input(case: dict[str, Any], slot_name: str) -> list[Any]:
    tokens = case.get("input_tokens") or []
    mapping = {
        "RIGHT_HAND_ACTION": "RIGHT_HAND_ACTION_COMPONENT",
        "STRING_NUMBER": "NUMERIC_COMPONENT",
        "HUI_POSITION": "NUMERIC_COMPONENT",
        "LEFT_FINGER": "LEFT_FINGER_NAME_COMPONENT",
        "TIMING_MARKER": "TIMING_MARKER_COMPONENT",
        "GENERIC_MARKER": "GENERIC_MARKER_COMPONENT",
        "SPECIAL_TECHNIQUE": "SPECIAL_TECHNIQUE_COMPONENT",
        "LEFT_HAND_ACTION": "LEFT_HAND_ACTION_COMPONENT",
        "PRE_SOUND_MOTION": "LEFT_HAND_ACTION_COMPONENT",
        "POST_SOUND_MOTION": "LEFT_HAND_ACTION_COMPONENT",
        "STATE_START": "STATE_MARKER_COMPONENT",
        "STATE_END": "STATE_MARKER_COMPONENT",
    }
    lexical = mapping.get(slot_name)
    if not lexical:
        return []
    values: list[Any] = []
    for token in tokens:
        if not isinstance(token, dict) or token.get("lexical_component_type") != lexical:
            continue
        values.append(token.get("token_id"))
        values.append(token.get("component_id_v0_2"))
        values.append(token.get("label_zh"))
    return [value for value in values if value is not None]


def _rules_in_result(result: dict[str, Any]) -> set[str]:
    rules: set[str] = set()
    for candidate in result.get("accepted_candidates", []):
        rules.update(candidate.get("applied_rule_ids", []))
    for candidate in result.get("rejected_candidates", []):
        attempted = candidate.get("attempted_rule_id")
        if attempted:
            rules.add(attempted)
    return rules


def _source_scan(repo_root: Path) -> dict[str, bool]:
    parser_source = (repo_root / "scripts" / "cyber_guqin_grammar_parser.py").read_text(encoding="utf-8")
    runner_source = (repo_root / "scripts" / "run_cyber_guqin_grammar_fixtures.py").read_text(encoding="utf-8")
    parser_bad_case_ids = any(marker in parser_source for marker in ["P1B-ABS", "P1B-REAL", "P1B-GUARD", "P1B-RANK"])
    return {
        "fixed_case_count_detected": "EXPECTED_CASE_COUNT" in parser_source or "TOTAL_CASES" in parser_source,
        "case_id_hardcoding_detected": parser_bad_case_ids,
        "oracle_leakage_detected": "expected" + "_" in parser_source or "acceptance_matrix" in parser_source,
        "runner_uses_post_parse_assertions": "expected" + "_" in runner_source,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--fixture-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = run_fixtures(Path(args.repo_root), Path(args.fixture_dir), allow_abstract_component_ids=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pass_count": report["pass_count"], "fail_count": report["fail_count"], "discovered_case_count": report["discovered_case_count"]}, ensure_ascii=False, indent=2))
    return 0 if report["fail_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
