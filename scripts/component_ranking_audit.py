#!/usr/bin/env python3
"""Component-level visual ranking audit for P2G/P2B outputs.

This module evaluates whether reviewed component ids appear in P2B Top-K
candidates for visual regions. It is not phrase reading authority, grammar
authority, score authority, or Dapu IR authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.p2g_component_lattice_runtime import P2GComponentLatticeRuntime
from scripts.visual_decomposition_runtime import VisualDecomposer


CONTRACT_ID = "CG_LXY_P2B_component_ranking_audit.v0.1"

AUTHORITY_FLAGS = {
    "VISUAL_COMPONENT_EVAL_ONLY": True,
    "NOT_PHRASE_READING_AUTHORITY": True,
    "NOT_GRAMMAR_AUTHORITY": True,
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
    "NEEDS_HUMAN_REVIEW": True,
}

FORBIDDEN_FIXTURE_KEYS = {
    "phrase_reading",
    "surface_reading",
    "canonical_reading",
    "complete_reading",
    "grammar_candidate",
    "grammar_parse",
    "score_fact",
    "score_event",
    "dapu_ir",
    "Dapu_IR",
    "work_title",
    "piece_title",
    "phrase_id",
    "phrase",
}


def validate_visual_component_eval_fixture(fixture: dict[str, Any], *, return_errors: bool = False) -> bool | list[str]:
    errors: list[str] = []
    required = {"fixture_id", "image_reference", "notation_unit_id", "expected_regions"}
    missing = sorted(required - set(fixture))
    if missing:
        errors.append(f"missing fixture keys: {missing}")
    forbidden = _find_forbidden_keys(fixture)
    for key in sorted(forbidden):
        errors.append(f"forbidden phrase/grammar field present: {key}")
    for index, region in enumerate(fixture.get("expected_regions") or []):
        if not isinstance(region, dict):
            errors.append(f"expected_regions[{index}] must be object")
            continue
        if region.get("review_purpose") != "P2G_P2B_VISUAL_EVAL_ONLY":
            errors.append(f"expected_regions[{index}] review_purpose must be P2G_P2B_VISUAL_EVAL_ONLY")
        if "reviewed_component_id" not in region and region.get("atlas_status") not in {
            "NO_INDEPENDENT_COMPONENT_ID",
            "MATCHABLE_FALSE",
            "COMPONENT_ATLAS_GAP",
        }:
            errors.append(f"expected_regions[{index}] must include reviewed_component_id or atlas_status gap")
    return errors if return_errors else not errors


class ComponentRankingAudit:
    """Evaluate component-level Top-K recall from a bridge result."""

    def audit_bridge_result(self, bridge_result: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
        errors = validate_visual_component_eval_fixture(fixture, return_errors=True)
        if errors:
            return self._invalid_fixture_report(fixture, bridge_result, errors)

        expected_regions = list(fixture.get("expected_regions") or [])
        mode = "VISUAL_SANITY_ONLY" if not _reviewed_regions(expected_regions) else "COMPONENT_RECALL_EVAL"
        observed_by_region = {
            str((item.get("visual_region") or {}).get("region_id") or item.get("crop_id")): item
            for item in bridge_result.get("component_candidate_sets") or []
        }
        region_results = [
            _region_result(expected, observed_by_region.get(str(expected.get("region_id"))))
            for expected in expected_regions
        ]
        observed_unreviewed = [
            _observed_region_summary(item)
            for item in bridge_result.get("component_candidate_sets") or []
            if str((item.get("visual_region") or {}).get("region_id") or item.get("crop_id"))
            not in {str(region.get("region_id")) for region in expected_regions}
        ]
        return {
            "contract_id": CONTRACT_ID,
            "fixture_id": fixture.get("fixture_id"),
            "image_reference": dict(fixture.get("image_reference") or {}),
            "notation_unit_id": fixture.get("notation_unit_id") or bridge_result.get("notation_unit_id"),
            "mode": mode,
            "region_results": region_results,
            "observed_unreviewed_regions": observed_unreviewed,
            "summary": _summary(region_results, bridge_result),
            "failure_flags": _failure_flags(region_results, errors=[]),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "audit_trace": {
                "runtime_layer": "P2B_COMPONENT_RANKING_AUDIT",
                "p1_parse_called": False,
                "p3_grammar_called": False,
                "phrase_oracle_used": False,
                "component_level_review_only": True,
            },
        }

    def run_fixture(
        self,
        fixture: dict[str, Any],
        *,
        top_k: int = 5,
        crop_output_dir: Path | str = "/private/tmp/cg_p2b_ranking_audit_crops",
    ) -> dict[str, Any]:
        image_ref = fixture.get("image_reference") or {}
        image_path = image_ref.get("path_or_uri") or image_ref.get("path")
        if not image_path:
            return self._invalid_fixture_report(fixture, {}, ["image_reference.path_or_uri is required"])
        decomposition = VisualDecomposer().decompose(image_path, notation_unit_id=str(fixture.get("notation_unit_id") or Path(image_path).stem))
        bridge = P2GComponentLatticeRuntime(crop_output_dir=crop_output_dir).build(decomposition, top_k=top_k)
        report = self.audit_bridge_result(bridge, fixture)
        report["p2g_summary"] = {
            "layout_candidates": decomposition.get("layout_candidates"),
            "quality_metrics": decomposition.get("quality_metrics"),
            "failure_flags": decomposition.get("failure_flags"),
        }
        report["bridge_summary"] = {
            "status": bridge.get("status"),
            "failure_flags": bridge.get("failure_flags"),
            "component_candidate_set_count": len(bridge.get("component_candidate_sets") or []),
        }
        return report

    def _invalid_fixture_report(
        self,
        fixture: dict[str, Any],
        bridge_result: dict[str, Any],
        errors: list[str],
    ) -> dict[str, Any]:
        return {
            "contract_id": CONTRACT_ID,
            "fixture_id": fixture.get("fixture_id"),
            "notation_unit_id": fixture.get("notation_unit_id") or bridge_result.get("notation_unit_id"),
            "mode": "INVALID_FIXTURE",
            "region_results": [],
            "observed_unreviewed_regions": [],
            "summary": {
                "reviewed_region_count": 0,
                "observed_region_count": len(bridge_result.get("component_candidate_sets") or []),
                "top1_hit_count": 0,
                "top3_hit_count": 0,
                "top5_hit_count": 0,
                "missing_count": 0,
                "atlas_gap_count": 0,
            },
            "failure_flags": ["INVALID_VISUAL_COMPONENT_EVAL_FIXTURE"],
            "validation_errors": list(errors),
            "authority_flags": dict(AUTHORITY_FLAGS),
            "audit_trace": {
                "runtime_layer": "P2B_COMPONENT_RANKING_AUDIT",
                "p1_parse_called": False,
                "p3_grammar_called": False,
                "phrase_oracle_used": False,
                "component_level_review_only": True,
            },
        }


def _region_result(expected: dict[str, Any], observed: dict[str, Any] | None) -> dict[str, Any]:
    reviewed_id = expected.get("reviewed_component_id")
    atlas_status = expected.get("atlas_status") or "HAS_COMPONENT_ID"
    base = {
        "region_id": expected.get("region_id"),
        "visual_role": expected.get("visual_role"),
        "bbox": list(expected.get("bbox") or []),
        "reviewed_component_id": reviewed_id,
        "reviewed_component_label": expected.get("reviewed_component_label"),
        "atlas_status": atlas_status,
    }
    if atlas_status in {"NO_INDEPENDENT_COMPONENT_ID", "MATCHABLE_FALSE", "COMPONENT_ATLAS_GAP"}:
        base.update(
            {
                "evaluation_status": "ATLAS_GAP",
                "rank_1_based": None,
                "pass_level": "ATLAS_GAP",
                "top_candidates": _top_candidates(observed),
            }
        )
        return base
    if not reviewed_id:
        base.update(
            {
                "evaluation_status": "UNREVIEWED_COMPONENT",
                "rank_1_based": None,
                "pass_level": "SKIPPED",
                "top_candidates": _top_candidates(observed),
            }
        )
        return base
    if observed is None:
        base.update(
            {
                "evaluation_status": "REGION_NOT_OBSERVED",
                "rank_1_based": None,
                "pass_level": "MISS",
                "top_candidates": [],
            }
        )
        return base

    candidates = list(observed.get("candidates") or [])
    ids = [candidate.get("component_id") for candidate in candidates]
    rank = ids.index(reviewed_id) + 1 if reviewed_id in ids else None
    top_score = _candidate_score(candidates[0]) if candidates else None
    reviewed_score = _candidate_score(candidates[rank - 1]) if rank else None
    score_gap = round(float(top_score) - float(reviewed_score), 3) if top_score is not None and reviewed_score is not None else None
    base.update(
        {
            "evaluation_status": "EVALUATED",
            "rank_1_based": rank,
            "pass_level": _pass_level(rank),
            "score_gap_to_top": score_gap,
            "top_candidates": _top_candidates(observed),
        }
    )
    return base


def _top_candidates(observed: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not observed:
        return []
    out = []
    for index, candidate in enumerate(observed.get("candidates") or [], start=1):
        out.append(
            {
                "rank_1_based": index,
                "component_id": candidate.get("component_id"),
                "label": candidate.get("label"),
                "confidence": _candidate_score(candidate),
                "visual_score": candidate.get("visual_score"),
            }
        )
    return out


def _observed_region_summary(candidate_set: dict[str, Any]) -> dict[str, Any]:
    region = candidate_set.get("visual_region") or {}
    return {
        "region_id": region.get("region_id") or candidate_set.get("crop_id"),
        "visual_role": region.get("visual_role"),
        "bbox": list(region.get("bbox") or []),
        "top_candidates": _top_candidates(candidate_set),
    }


def _candidate_score(candidate: dict[str, Any]) -> float:
    score = (candidate.get("score_breakdown") or {}).get("final", candidate.get("visual_score", 0.0))
    try:
        return round(float(score), 3)
    except (TypeError, ValueError):
        return 0.0


def _pass_level(rank: int | None) -> str:
    if rank is None:
        return "MISS"
    if rank == 1:
        return "PASS_TOP1"
    if rank <= 3:
        return "PASS_TOP3"
    if rank <= 5:
        return "PASS_TOP5"
    return "MISS"


def _summary(region_results: list[dict[str, Any]], bridge_result: dict[str, Any]) -> dict[str, int]:
    evaluated = [item for item in region_results if item.get("evaluation_status") == "EVALUATED"]
    return {
        "reviewed_region_count": len(evaluated),
        "observed_region_count": len(bridge_result.get("component_candidate_sets") or []),
        "top1_hit_count": sum(1 for item in evaluated if item.get("rank_1_based") == 1),
        "top3_hit_count": sum(1 for item in evaluated if item.get("rank_1_based") and item["rank_1_based"] <= 3),
        "top5_hit_count": sum(1 for item in evaluated if item.get("rank_1_based") and item["rank_1_based"] <= 5),
        "missing_count": sum(1 for item in evaluated if item.get("rank_1_based") is None),
        "atlas_gap_count": sum(1 for item in region_results if item.get("evaluation_status") == "ATLAS_GAP"),
    }


def _failure_flags(region_results: list[dict[str, Any]], *, errors: list[str]) -> list[str]:
    flags = []
    if errors:
        flags.append("INVALID_VISUAL_COMPONENT_EVAL_FIXTURE")
    if any(item.get("pass_level") == "MISS" for item in region_results):
        flags.append("P2B_RECALL_MISS")
    if any(item.get("evaluation_status") == "ATLAS_GAP" for item in region_results):
        flags.append("COMPONENT_ATLAS_GAP")
    return flags


def _reviewed_regions(regions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [region for region in regions if region.get("reviewed_component_id")]


def _find_forbidden_keys(value: Any) -> set[str]:
    seen: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in FORBIDDEN_FIXTURE_KEYS:
                seen.add(str(key))
            seen.update(_find_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value:
            seen.update(_find_forbidden_keys(child))
    return seen


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run component-level P2B ranking audit from visual eval fixtures.")
    parser.add_argument("fixture_json")
    parser.add_argument("--output")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--crop-output-dir", default="/private/tmp/cg_p2b_ranking_audit_crops")
    args = parser.parse_args(argv)

    payload = json.loads(Path(args.fixture_json).read_text(encoding="utf-8"))
    fixtures = payload.get("fixtures") if isinstance(payload, dict) and "fixtures" in payload else [payload]
    audit = ComponentRankingAudit()
    reports = [audit.run_fixture(fixture, top_k=args.top_k, crop_output_dir=args.crop_output_dir) for fixture in fixtures]
    result = {
        "contract_id": "CG_LXY_P2B_component_ranking_audit_batch.v0.1",
        "fixture_count": len(fixtures),
        "reports": reports,
        "authority_flags": dict(AUTHORITY_FLAGS),
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
