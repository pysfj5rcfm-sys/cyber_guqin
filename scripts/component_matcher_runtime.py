#!/usr/bin/env python3
"""P2 runtime component matcher facade with non-oracle score breakdowns."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.component_matcher import ComponentMatcher as TemplateComponentMatcher
from scripts.component_visual_index import ComponentVisualIndex, DEFAULT_OUTPUT


AUTHORITY_FLAGS = {
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_CANON_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}

SLOT_ALLOWED_LEXICAL_TYPES = {
    "LEFT_FINGER": {"LEFT_FINGER_NAME_COMPONENT"},
    "HUI_POSITION": {"NUMERIC_COMPONENT", "POSITION_COMPONENT"},
    "RIGHT_HAND_ACTION": {"RIGHT_HAND_ACTION_COMPONENT"},
    "STRING_NUMBER": {"NUMERIC_COMPONENT"},
    "SOUND_STATE": {"STATE_MARKER_COMPONENT"},
    "TIMING_MARKER": {"TIMING_MARKER_COMPONENT"},
    "GENERIC_MARKER": {"GENERIC_MARKER_COMPONENT"},
}


class ComponentMatcher:
    """Deterministic single-crop matcher for ComponentCandidateSet output."""

    def __init__(
        self,
        image_index: ComponentVisualIndex,
        *,
        unknown_threshold: float = 0.45,
        ambiguity_margin: float = 0.025,
    ) -> None:
        self.image_index = image_index
        self.unknown_threshold = float(unknown_threshold)
        self.ambiguity_margin = float(ambiguity_margin)
        self._template_matcher = TemplateComponentMatcher(
            image_index,
            unknown_threshold=unknown_threshold,
            ambiguity_margin=ambiguity_margin,
        )

    def match(
        self,
        crop: Path | str,
        top_k: int = 5,
        crop_id: str | None = None,
        grammar_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        base = self._template_matcher.match(crop, top_k=top_k, crop_id=crop_id)
        if base.get("status") == "UNKNOWN_COMPONENT":
            return self._unknown_from_base(base)

        candidates = [
            self._candidate_from_base(item, grammar_context or {})
            for item in base.get("candidates", [])
        ]
        candidates.sort(
            key=lambda item: (
                -item["score_breakdown"]["final"],
                -item["visual_score"],
                item["component_id"],
            )
        )
        for rank, candidate in enumerate(candidates):
            candidate["rank"] = rank

        status = "MATCHED"
        if len(candidates) > 1:
            final_gap = candidates[0]["score_breakdown"]["final"] - candidates[1]["score_breakdown"]["final"]
            if final_gap <= self.ambiguity_margin:
                status = "AMBIGUOUS"

        ranking = {candidate["component_id"]: dict(candidate["score_breakdown"]) for candidate in candidates}
        matched_components = [candidate["component_id"] for candidate in candidates]
        result = {
            "crop_id": base.get("crop_id"),
            "status": status,
            "candidates": candidates,
            "ranking": ranking,
            "unknown_component_state": {
                "status": "NOT_UNKNOWN",
                "unresolved_reason": None,
                "needs_human_review": True,
            },
            "coverage_ledger": {
                "crop_id": base.get("crop_id"),
                "matched_components": matched_components,
                "unresolved_reason": None,
                "needs_human_review": True,
            },
            "authority_flags": dict(AUTHORITY_FLAGS),
            "matcher_trace": self._matcher_trace(base, len(candidates)),
        }
        return result

    def can_fit(self, component_candidate: dict[str, Any], slot_context: dict[str, Any] | None = None) -> bool:
        return _grammar_compatibility(component_candidate, slot_context or {}) >= 0.5

    def _candidate_from_base(
        self,
        base_candidate: dict[str, Any],
        grammar_context: dict[str, Any],
    ) -> dict[str, Any]:
        visual = _visual_score(base_candidate)
        lexical_type = infer_lexical_component_type(base_candidate.get("category", ""))
        shell_candidate = {
            "component_id": base_candidate.get("component_id"),
            "label": base_candidate.get("label", ""),
            "category": base_candidate.get("category", ""),
            "lexical_component_type": lexical_type,
        }
        lexical = _lexical_compatibility(shell_candidate, grammar_context)
        grammar = _grammar_compatibility(shell_candidate, grammar_context.get("slot_context") or grammar_context)
        penalty = _uncertainty_penalty(base_candidate, grammar_context)
        final = _clamp(0.68 * visual + 0.18 * lexical + 0.14 * grammar - penalty)
        breakdown = {
            "visual": round(visual, 3),
            "lexical": round(lexical, 3),
            "grammar": round(grammar, 3),
            "uncertainty_penalty": round(penalty, 3),
            "final": round(final, 3),
        }
        return {
            "component_id": shell_candidate["component_id"],
            "label": shell_candidate["label"],
            "category": shell_candidate["category"],
            "lexical_component_type": lexical_type,
            "visual_score": round(visual, 3),
            "rank": int(base_candidate.get("rank", 1)) - 1,
            "evidence": dict(base_candidate.get("evidence") or {}),
            "score_breakdown": breakdown,
        }

    def _unknown_from_base(self, base: dict[str, Any]) -> dict[str, Any]:
        trace = dict(base.get("matcher_trace") or {})
        warnings = list(trace.get("warnings") or [])
        failure = trace.get("failure_classification") or "UNKNOWN_THRESHOLD_ERROR"
        if failure == "INPUT_FORMAT_ERROR" and "EMPTY_IMAGE" in warnings:
            unresolved = "INSUFFICIENT_VISUAL_EVIDENCE"
        elif failure == "INPUT_FORMAT_ERROR":
            unresolved = "UNKNOWN_COMPONENT"
        elif failure == "IMAGE_INDEX_ERROR":
            unresolved = "SOURCE_REFERENCE_GAP"
        else:
            unresolved = "UNKNOWN_COMPONENT"
        return {
            "crop_id": base.get("crop_id"),
            "status": "UNKNOWN_COMPONENT",
            "candidates": [],
            "ranking": {},
            "unknown_component_state": {
                "status": "UNKNOWN_COMPONENT",
                "unresolved_reason": unresolved,
                "needs_human_review": True,
            },
            "coverage_ledger": {
                "crop_id": base.get("crop_id"),
                "matched_components": [],
                "unresolved_reason": unresolved,
                "needs_human_review": True,
            },
            "authority_flags": dict(AUTHORITY_FLAGS),
            "matcher_trace": self._matcher_trace(base, 0),
        }

    def _matcher_trace(self, base: dict[str, Any], top_k_returned: int) -> dict[str, Any]:
        trace = dict(base.get("matcher_trace") or {})
        trace.update(
            {
                "runtime_layer": "P2_VISUAL_COMPONENT_LAYER_MVP",
                "p1_parse_called": False,
                "random_model_used": False,
                "external_model_downloaded": False,
                "score_formula": "0.68*visual + 0.18*lexical + 0.14*grammar - uncertainty_penalty",
                "top_k_returned": top_k_returned,
            }
        )
        return trace


def infer_lexical_component_type(category: str) -> str:
    value = (category or "").lower()
    if "numeric" in value:
        return "NUMERIC_COMPONENT"
    if "left_finger_name" in value:
        return "LEFT_FINGER_NAME_COMPONENT"
    if value.startswith("right_hand") or "right_hand" in value:
        return "RIGHT_HAND_ACTION_COMPONENT"
    if value.startswith("left_hand") or "left_hand" in value:
        return "LEFT_HAND_ACTION_COMPONENT"
    if "sound_position" in value or "state_marker" in value:
        return "STATE_MARKER_COMPONENT"
    if "rhythm" in value or "timing" in value:
        return "TIMING_MARKER_COMPONENT"
    if "generic" in value:
        return "GENERIC_MARKER_COMPONENT"
    if "position" in value:
        return "POSITION_COMPONENT"
    if "special" in value:
        return "SPECIAL_TECHNIQUE_COMPONENT"
    return "UNKNOWN_COMPONENT"


def _visual_score(candidate: dict[str, Any]) -> float:
    evidence = candidate.get("evidence") or {}
    similarity = evidence.get("visual_similarity") or {}
    value = similarity.get("rank_score", 0.0)
    try:
        return _clamp(float(value))
    except (TypeError, ValueError):
        return 0.0


def _lexical_compatibility(candidate: dict[str, Any], context: dict[str, Any]) -> float:
    lexical_type = candidate.get("lexical_component_type") or "UNKNOWN_COMPONENT"
    allowed = set(context.get("allowed_lexical_types") or [])
    if allowed:
        return 1.0 if lexical_type in allowed else 0.2
    allowed_categories = set(context.get("allowed_categories") or [])
    if allowed_categories:
        return 1.0 if candidate.get("category") in allowed_categories else 0.2
    return 0.4 if lexical_type == "UNKNOWN_COMPONENT" else 1.0


def _grammar_compatibility(candidate: dict[str, Any], slot_context: dict[str, Any]) -> float:
    if not slot_context:
        return 0.6
    component_id = candidate.get("component_id")
    allowed_ids = set(slot_context.get("allowed_component_ids") or [])
    if allowed_ids:
        return 1.0 if component_id in allowed_ids else 0.0
    slot_id = slot_context.get("slot_id")
    if slot_id:
        allowed = SLOT_ALLOWED_LEXICAL_TYPES.get(str(slot_id), set())
        if allowed:
            return 1.0 if candidate.get("lexical_component_type") in allowed else 0.0
    allowed_lexical = set(slot_context.get("allowed_lexical_types") or [])
    if allowed_lexical:
        return 1.0 if candidate.get("lexical_component_type") in allowed_lexical else 0.0
    return 0.6


def _uncertainty_penalty(candidate: dict[str, Any], context: dict[str, Any]) -> float:
    penalty = 0.0
    if candidate.get("confidence_level") == "LOW":
        penalty += 0.08
    evidence = candidate.get("evidence") or {}
    if not evidence.get("source_image_reference"):
        penalty += 0.05
    if context.get("uncertainty_penalty"):
        try:
            penalty += float(context["uncertainty_penalty"])
        except (TypeError, ValueError):
            penalty += 0.0
    return _clamp(penalty)


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def load_default_matcher(
    *,
    index_path: Path | str = DEFAULT_OUTPUT,
    repo_root: Path | str = REPO_ROOT,
    unknown_threshold: float = 0.45,
) -> ComponentMatcher:
    return ComponentMatcher(
        ComponentVisualIndex.from_file(index_path, repo_root=repo_root),
        unknown_threshold=unknown_threshold,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run P2 runtime component matcher on one crop image.")
    parser.add_argument("image_crop")
    parser.add_argument("--index", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--repo-root", default=str(REPO_ROOT))
    parser.add_argument("--crop-id")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--unknown-threshold", type=float, default=0.45)
    args = parser.parse_args(argv)

    matcher = load_default_matcher(
        index_path=args.index,
        repo_root=args.repo_root,
        unknown_threshold=args.unknown_threshold,
    )
    result = matcher.match(args.image_crop, crop_id=args.crop_id, top_k=args.top_k)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
